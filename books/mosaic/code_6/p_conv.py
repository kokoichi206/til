import tensorflow as tf
import os

from tensorflow.keras import backend as K
import tensorflow.keras.layers as layers
import pickle
import numpy as np
import time
from PIL import Image

from inpainting_layers import RegionNormL, RegionNormB, upsampling2d_tpu, PConv2D
from utils import Reduction, distributed, make_grid, make_citation

import utils
utils.strategy = strategy

def load_dataset(batch_size):
    def preprocess(x):
        if x.shape[-1] == 1:
            x = tf.broadcast_to(x, (*x.shape[:-1], 3))
        return tf.image.convert_image_dtype(x, tf.float32)

    train = np.load("train.npz")
    n = len(train["image"]) // 2
    trains = (
        tf.constant(train["image"][:n]), tf.constant(train["image"][n:2*n]),
        tf.constant(train["mosaic"][:n]), tf.constant(train["mosaic"][n:2*n]),
        tf.constant(train["mask"][:n]), tf.constant(train["mask"][n:2*n])
    )
    # TF2.5↑：batchにdrop_remainder=Trueをつける
    trainset = tf.data.Dataset.from_tensor_slices(trains).map(
        lambda *args: [preprocess(a) for a in args]
    ).shuffle(512).batch(batch_size // 2, drop_remainder=True).prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
    val = np.load("test.npz", allow_pickle=True)
    valset = tf.data.Dataset.from_tensor_slices((val["image"], val["mosaic"], val["mask"]))
    valset = valset.map(
        lambda *args: [preprocess(a) for a in args]
    ).batch(batch_size, drop_remainder=True).prefetch(buffer_size=tf.data.experimental.AUTOTUNE)     
    return trainset, valset, val["json"]

## Pconv Unet
def pconv_unet(use_region_wise):
    input_image = tf.keras.layers.Input((256, 256, 3))    
    input_mask = tf.keras.layers.Input((256, 256, 3))
    # encoder
    enc_filter_sizes = [7, 5, 5, 3, 3, 3, 3]
    base_ch = 50 if use_region_wise else 64
    enc_channels = [base_ch * i for i in [1, 2, 4, 8, 8, 8, 8]]    
    x, m = input_image, input_mask
    enc_images, enc_masks = [], []
    for i in range(len(enc_channels)):
        if use_region_wise:
            x1, m = PConv2D(enc_channels[i], enc_filter_sizes[i], strides=2)([x, m])
            x2 = layers.Conv2D(enc_channels[i], enc_filter_sizes[i], strides=2, padding="same")(x)
            x = layers.Lambda(lambda z: z[0] * z[2] + z[1] * (1 - z[2]))([x2, x1, m])
        else:
            x, m = PConv2D(enc_channels[i], enc_filter_sizes[i], strides=2)([x, m])

        if i != 0:
            if use_region_wise:
                x = RegionNormB()([x, m])
            else:
                x = layers.BatchNormalization()(x)
        x = layers.ReLU()(x)
        if i != len(enc_channels) - 1:                
            enc_images.append(x)
            enc_masks.append(m)

    # Decoder
    for i in range(len(enc_channels) - 2, -1, -1):
        cnt = len(enc_channels) - i        
        x = layers.Lambda(upsampling2d_tpu, name="UpsamplingImage_"+str(cnt))(x)
        m = layers.Lambda(upsampling2d_tpu, name="UpsamplingMask"+str(cnt))(m)
        x = layers.Concatenate()([x, enc_images[i]])
        m = layers.Concatenate()([m, enc_masks[i]])

        if use_region_wise:
            x1, m = PConv2D(enc_channels[i], kernel_size=3)([x, m])
            x2 = layers.Conv2D(enc_channels[i], kernel_size=3, padding="same")(x)
            x = layers.Lambda(lambda z: z[0] * z[2] + z[1] * (1 - z[2]))([x2, x1, m])  # 0 = hole
            x = RegionNormL()(x)
        else:
            x, m = PConv2D(enc_channels[i], kernel_size=3)([x, m])
            x = layers.BatchNormalization()(x)    
        x = layers.LeakyReLU(0.2)(x)

    # Concat with Input
    x = layers.Lambda(upsampling2d_tpu, name="UpsamplingImage_1")(x)
    m = layers.Lambda(upsampling2d_tpu, name="UpsamplingMask_1")(m)
    x = layers.Concatenate()([x, input_image])
    m = layers.Concatenate()([m, input_mask])
    if use_region_wise:
        x1, m = PConv2D(3, kernel_size=3)([x, m])
        x2 = layers.Conv2D(3, kernel_size=3, padding="same")(x)
        x = layers.Lambda(lambda z: z[0] * z[2] + z[1] * (1 - z[2]))([x2, x1, m])
    else:
        x, m = PConv2D(3, kernel_size=3)([x, m])
    x = layers.Activation("sigmoid")(x)
    return tf.keras.models.Model([input_image, input_mask], x)

## VGG16
def create_vgg16():
    model = tf.keras.applications.VGG16(input_shape=(256, 256, 3), include_top=False, weights="imagenet")
    # [3,6,10] - [pool1, pool2, pool3]
    outputs = [model.layers[i].output for i in [3, 6, 10]]
    model = tf.keras.models.Model(model.inputs, outputs)
    model.trainable = False
    return model

def get_vgg16_features(model, inputs):
    # caffe scale
    # [103.939, 116.779, 123.68] mean shift on [0-255], [BGR]    
    mean_shift = tf.reshape(tf.constant([103.939, 116.779, 123.68], inputs.dtype), [1, 1, 1, 3])    
    x = inputs[:,:,:,::-1] * 255.0 - mean_shift
    outs = model(x, training=False)
    return [x / 255.0 for x in outs]  # feature scaling (暫定的措置)    
    
## Loss
def total_loss(y_true, y_pred, mask, vgg_model):
    vgg_true = get_vgg16_features(vgg_model, y_true)
    vgg_pred = get_vgg16_features(vgg_model, y_pred)
    y_comp = mask * y_true + (1 - mask) * y_pred
    vgg_comp = get_vgg16_features(vgg_model, y_comp)

    def l1(a, b):
        return tf.reduce_mean(tf.abs(a - b), axis=[i for i in range(1, len(a.shape))])      

    def gram_matrix(x, norm_by_channels=False):
        """Calculate gram matrix used in style loss"""
        
        # Assertions on input
        assert K.ndim(x) == 4, 'Input tensor should be a 4d (B, H, W, C) tensor'
        assert K.image_data_format() == 'channels_last', "Please use channels-last format"        
        
        # Permute channels and get resulting shape
        x = K.permute_dimensions(x, (0, 3, 1, 2))
        shape = K.shape(x)
        B, C, H, W = shape[0], shape[1], shape[2], shape[3]
        
        # Reshape x and do batch dot product
        features = K.reshape(x, K.stack([B, C, H*W]))
        gram = K.batch_dot(features, features, axes=2)
        
        # Normalize with channels, height and width
        gram = gram /  K.cast(C * H * W, x.dtype)
        
        return gram

    def loss_hole():
        return l1((1 - mask) * y_true, (1 - mask) * y_pred)
    
    def loss_valid():
        return l1(mask * y_true, mask * y_pred)
        
    def loss_perceptual():
        loss = 0
        for p, c, t in zip(vgg_pred, vgg_comp, vgg_true):
            loss += l1(p, t) + l1(c, t)
        return loss

    def loss_style(mat_a, mat_b):
        loss = 0
        for a, b in zip(mat_a, mat_b):
            loss += l1(gram_matrix(a), gram_matrix(b))
        return loss

    def loss_tv():
        """Total variation loss, used for smoothing the hole region, see. eq. 6"""

        # Create dilated hole region using a 3x3 kernel of all 1s.
        kernel = tf.ones(shape=(3, 3, mask.shape[3], mask.shape[3]))
        dilated_mask = K.conv2d(1-mask, kernel, data_format='channels_last', padding='same')

        # Cast values to be [0., 1.], and compute dilated hole region of y_comp
        dilated_mask = K.cast(K.greater(dilated_mask, 0), 'float32')
        P = dilated_mask * y_comp

        # Calculate total variation loss
        a = l1(P[:,1:,:,:], P[:,:-1,:,:])
        b = l1(P[:,:,1:,:], P[:,:,:-1,:])        
        return a+b

    ## loss component
    loss1 = loss_valid()
    loss2 = loss_hole()
    loss3 = loss_perceptual()
    loss4 = loss_style(vgg_pred, vgg_true)
    loss5 = loss_style(vgg_comp, vgg_true)
    loss6 = loss_tv()

    return loss1 + 6 * loss2 + 0.05 * loss3 + 120 * (loss4 + loss5) + 0.1 * loss6
###

def main(use_regionwise, fine_tuning=False):
    batch_size = 32
    n_sampling = 180
    trainset, valset, valjson = load_dataset(batch_size)
    citations = make_citation(valjson[:n_sampling], 256).astype(np.float32) / 255.0

    with strategy.scope():
        custom_objects = {"PConv2D": PConv2D}
        if use_regionwise:
            custom_objects.update({"RegionNormL": RegionNormL, "RegionNormB": RegionNormB})  

        if os.path.exists("model.h5"):
            model = tf.keras.models.load_model("model.h5", custom_objects=custom_objects)
        else:
            model = pconv_unet(use_regionwise)
        vgg = create_vgg16()

        if fine_tuning:
            for l in model.layers:
                if isinstance(l, layers.BatchNormalization):
                    l.trainable = False
            optim = tf.keras.optimizers.Adam(learning_rate=5e-5)
        else:
            optim = tf.keras.optimizers.Adam(learning_rate=2e-4)

        trainset = strategy.experimental_distribute_dataset(trainset)
        valset = strategy.experimental_distribute_dataset(valset)

        @distributed(Reduction.SUM)        
        def train_on_batch(args):
            loss_accum = 0
            n = len(args) // 3
            for i in range(n):
                images, mosaic, masks = args[i], args[i + n], args[i + 2 * n]
                # backprop
                with tf.GradientTape() as tape:
                    pred = model([mosaic, masks], training=True)
                    loss = total_loss(images, pred, masks, vgg)
                    loss = tf.reduce_sum(loss) * (1.0 / batch_size)
                grads = tape.gradient(loss, model.trainable_weights)
                optim.apply_gradients(zip(grads, model.trainable_weights))
                loss_accum += loss
            return loss_accum

        @distributed(Reduction.SUM, Reduction.CONCAT, Reduction.CONCAT, Reduction.CONCAT, Reduction.CONCAT, Reduction.MEAN, Reduction.MEAN)
        def validation_on_batch(images, mosaic, masks):
            pred = model([mosaic, masks], training=False)
            loss = total_loss(images, pred, masks, vgg)
            loss = tf.reduce_sum(loss) * (1.0 / batch_size)
            # metrics
            comp = images * masks + pred * (1 - masks)         
            psnr = tf.reduce_mean(tf.image.psnr(images, comp, max_val=1.0), axis=-1)
            msssim = tf.reduce_mean(tf.image.ssim_multiscale(images, comp, max_val=1.0), keepdims=True)
            return loss, images, mosaic, pred, comp, psnr, msssim

        result = {"train_loss": [], "val_loss": [], "val_psnr": [], "val_msssim": []}
        start_time = time.time()

        for epoch in range(10):
            train_losses = []
            for step, args in enumerate(trainset):
                train_losses.append(train_on_batch(args).numpy())
            
            val_tmps = [[] for i in range(7)]
            for step, (image, mos, mask) in enumerate(valset):
                # loss, images, mosaic, pred, comp, psnr, msssim
                val_results = validation_on_batch(image, mos, mask)

                for i in [0, -1, -2]:
                    val_tmps[i].append(val_results[i].numpy())

                if step < n_sampling // batch_size + 1:
                    for i in range(1, 5):
                        val_tmps[i].append(val_results[i].numpy())
            
            # URLを追加
            train_losses = np.mean(np.array(train_losses))
            for i in [0, -1, -2]:
                val_tmps[i] = np.mean(np.array(val_tmps[i]))
            for i in range(1, 5):
                val_tmps[i] = np.concatenate(val_tmps[i], axis=0)[:n_sampling]

            print(f"Epoch = {epoch+1}, loss = {train_losses}, val_loss = {val_tmps[0]}, val_psnr = {val_tmps[-2]}, val_msssim = {val_tmps[-1]}, time = {time.time()-start_time:.0f}")
            
            if min(result["val_loss"] + [np.inf]) > val_tmps[0]:
                print(f"New record ! {min(result['val_loss'] + [np.inf])} -> {val_tmps[0]}, " +
                    f"psnr = {max(result['val_psnr'] + [0.0])} -> {val_tmps[-2]}")
                
                sampling = np.stack(val_tmps[1:5] + [citations], axis=1)         
                sampling = sampling.reshape(-1, *sampling.shape[2:])
                sampling = (sampling * 255.0).astype(np.uint8)

                out_dir = mask_mode+"_pconv_rw_"+str(use_regionwise)
                if not os.path.exists(out_dir):
                    os.mkdir(out_dir)
                for i in range(n_sampling // 3):
                    grid = make_grid(sampling[i * 15:(i + 1) * 15], nrow=5, padding=15)
                    with Image.fromarray(grid) as img:
                        img.save(out_dir + f"/sampling_{i+1:03}.jpg", quality=95)

                model.save(out_dir + "/model.h5")

                np.savez_compressed(out_dir + "/sampling.npz", {"sampling": sampling})                

            result["train_loss"].append(train_losses)
            result["val_loss"].append(val_tmps[0])
            result["val_psnr"].append(val_tmps[-2])
            result["val_msssim"].append(val_tmps[-1])

    with open(out_dir + "/result.pkl", "wb") as fp:
        pickle.dump(result, fp)

if __name__ == "__main__":
    main(regionwise)
