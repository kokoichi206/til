## sec 10
Edge Connect によるモザイク除去

### Edge Connect
2つのネットワークからなる

1. マスク領域を補完したエッジ画像を作る
2. エッジ画像を着色する

人間にとって扱いやすい形でパイプラインを区切っているのが嬉しい！（線画だけ人間が描いて、着色の部分をNNがやる、ということができる）

### SkrGAN
Inpainting ではないが、「線画 → 着色」という2段階にGANを分割する発想

### エッジ検出
``` python
from PIL import Image, ImageFilter

# 変換をかける前にグレースケールに変換する
with Image.open("some_image.jpg") as img:
    edge = img.convert("L").filter(ImageFilter.FIND_EDGES())
```

DL の処理としても簡単に実装できる

#### Canny エッジ検出

``` python
import cv2

img = cv2.imread("some_image.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray, 100, 200)
```

#### 比較
- PIL によるエッジ検出は素直な形だが、線画としては線画細すぎる
- Canny エッジ検出はよりはっきりした線となるが、余計な線が目立つ
- アニメ画像のようなベタ塗りのケースでは、PIL のエッジ検出で十分なことも多い。


> 最も簡単なエッジ検出は、グレースケール化して畳み込みフィルターを１回適応する方法。

### Nol-Local Block (Self Attention)

### to gray scale
``` python
def to_grayscale(color_image):
    gray_kernel = np.array([0.299, 0.587, 0.114], np.float32).reshape(3, 1)
```


