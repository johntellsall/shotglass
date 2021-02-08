from git import Git, Repo
from PIL import Image, ImageDraw

# Bold Farmhouse https://www.color-hex.com/color-palette/104687
PALETTE = ["#830015", "#000068", "#8fb178", "#f2e8cf", "#ae976d"]


def line_count(path):
    return sum(1 for _ in open(path))


def ls_files(gitobj, pat):
    return gitobj.ls_files(pat).split("\n")


# TODO change to count index
def count_project(project):
    gitproj = Git(project)
    return {
        # "python": len(ls_files(gitproj, "*.py")),
        "html": len(ls_files(gitproj, "*.html")),
        "c": len(ls_files(gitproj, "*.[ch]")),
        # "test": len(ls_files(gitproj, "test*")),
        "total": len(ls_files(gitproj, "*")),
    }


project = "../SOURCE/redis/"


stats = count_project(project)

# import ipdb

# ipdb.set_trace()

img = Image.new("RGB", (100, 100), (88, 88, 88))

scale_x = img.width / stats["total"]
draw = ImageDraw.Draw(img)

cursor = 0
suffixes = ("c", "html")
labels = []

for i in range(len(suffixes)):
    suffix = suffixes[i]
    width = scale_x * stats[suffix]
    labels.append(dict(x=cursor + 3, y=20, text=suffix.upper()))
    draw.rectangle(
        [cursor, 0, width, img.height], fill=PALETTE[i], outline="gainsboro", width=2
    )
    cursor += width

for label in labels:
    draw.text([label["x"], label["y"]], label["text"], fill="white")

img.save("z.png", "PNG")