from PIL import Image

with Image.open("../target/jihyo.png") as orig:
    img = orig.resize((orig.width//8, orig.height//8), Image.NEAREST)
    img = img.resize(orig.size, Image.NEAREST)
    img.save('./nearest.png')


with Image.open("../target/jihyo.png") as orig:
    img = orig.resize((orig.width//8, orig.height//8), Image.BILINEAR)
    img = img.resize(orig.size, Image.BILINEAR)
    img.save('./bilinear.png')


with Image.open("../target/jihyo.png") as orig:
    img = orig.resize((orig.width//8, orig.height//8), Image.BICUBIC)
    img = img.resize(orig.size, Image.BICUBIC)
    img.save('./bicubic.png')

