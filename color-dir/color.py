from PIL import Image, ImageDraw

# with Image.open("z.jpg") as im:
img = Image.new("RGB", (100, 100), (250, 250, 250))

draw = ImageDraw.Draw(img)
draw.line((0, 0) + img.size, fill=128)
draw.line((0, img.size[1], img.size[0], 0), fill=128)

img.save("z.png", "PNG")