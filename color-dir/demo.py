from PIL import Image, ImageDraw

img = Image.new("RGB", (100, 100), (88, 88, 88))

draw = ImageDraw.Draw(img)
if 0:
    draw.line((0, 0) + img.size, fill="red")
    draw.line((0, img.size[1], img.size[0], 0), fill="blue")

if 0:
    draw.point((75, 50), fill="red")

draw.rectangle([20, 50, 30, 65], fill="green", outline="red", width=2)

if 0:
    draw.text([20, 50], "Beer", fill="black")

img.save("z.png", "PNG")