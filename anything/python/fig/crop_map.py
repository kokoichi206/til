from PIL import Image


im = Image.open("rpg_map.png")

ONE_BLOCK = 8
for i in range(16):
    start_x = (i % 4) * ONE_BLOCK
    start_y = (i // 4) * ONE_BLOCK
    im_crop = im.crop((start_x, start_y, start_x + ONE_BLOCK, start_y + ONE_BLOCK))
    im_crop.save(f"maps/map_{i}.png", quality=100)


im = Image.open("player.png")

ONE_BLOCK_X = 8
ONE_BLOCK_Y = 9
for i in range(8):
    start_x = (i % 2) * ONE_BLOCK_X
    start_y = (i // 2) * ONE_BLOCK_Y
    im_crop = im.crop((start_x, start_y, start_x + ONE_BLOCK_X, start_y + ONE_BLOCK_Y))
    im_crop.save(f"maps/player_{i}.png", quality=100)


im = Image.open("monster.png")

ONE_BLOCK_X = 8
ONE_BLOCK_Y = 9
for i in range(4):
    start_x = (i % 4) * ONE_BLOCK_X
    start_y = (i // 4) * ONE_BLOCK_Y
    im_crop = im.crop((start_x, start_y, start_x + ONE_BLOCK_X, start_y + ONE_BLOCK_Y))
    im_crop.save(f"maps/monster_{i}.png", quality=100)
