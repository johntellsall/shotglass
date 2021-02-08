from pathlib import Path
from git import Git, Repo
from PIL import Image, ImageDraw

# Bold Farmhouse https://www.color-hex.com/color-palette/104687
PALETTE = ["#830015", "#000068", "#8fb178", "#f2e8cf", "#ae976d"]


def line_count(path):
    return sum(1 for _ in open(path))


def ls_files(gitobj, pat):
    return gitobj.ls_files(pat).split("\n")


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
gitproj = Git(project)
source_names = ls_files(gitproj, "*.[ch]")
sourcedb = dict.fromkeys(source_names)
for name in sourcedb:
    sourcedb[name] = {"path": Path(gitproj.working_dir) / name}
for name, info in sourcedb.items():
    sourcedb[name]["line_count"] = line_count(info["path"])

total_lines = sum([info["line_count"] for info in sourcedb.values()])

img = Image.new("RGB", [1000] * 2, (88, 88, 88))

scale_x = img.width / total_lines
draw = ImageDraw.Draw(img)

cursor = 0
labels = []
important_width = img.width * 0.04

for i, name in enumerate(sourcedb):
    info = sourcedb[name]
    width = scale_x * info["line_count"]
    color = PALETTE[i % len(PALETTE)]

    if width > important_width:
        labels.append(dict(x=cursor + 3, y=20, text=name))

    draw.rectangle(
        [cursor, 0, cursor + width, img.height],
        fill=color,
        outline="gainsboro",
        width=2,
    )
    cursor += width

for label in labels:
    draw.text([label["x"], label["y"]], label["text"], fill="white")

img.save("z.png", "PNG")