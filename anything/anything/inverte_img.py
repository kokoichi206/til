from PIL import Image

def invert_colors(img_path, output_path):
    # 画像を開く
    img = Image.open(img_path)

    # ピクセルごとに色を反転する
    inverted_img = img.point(lambda p: 255 - p)

    # 反転した画像を保存
    inverted_img.save(output_path)

img_path = "me.jpg"
output_path = "inverted_me.jpg"
invert_colors(img_path, output_path)
