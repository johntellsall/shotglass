import argparse
import pprint
from pathlib import Path

from git import Git, Repo
from PIL import Image, ImageDraw


# Bold Farmhouse https://www.color-hex.com/color-palette/104687
PALETTE = ["#830015", "#000068", "#8fb178", "#f2e8cf", "#ae976d"]
# Dull Shell https://www.color-hex.com/color-palette/104668
# PALETTE = ["#dfb2b2", "#bf8a8a", "#b67777", "#985d5d", "#784343"]


def line_count(path):
    return sum(1 for _ in open(path))


def ls_files(gitobj, pat):
    return gitobj.ls_files(pat).split("\n")


def count_project(project):
    gitproj = Git(project)
    return {
        "python": len(ls_files(gitproj, "*.py")),
        "html": len(ls_files(gitproj, "*.html")),
        "c": len(ls_files(gitproj, "*.[ch]")),
        # "test": len(ls_files(gitproj, "test*")),
        "total": len(ls_files(gitproj, "*")),
    }


def cmd_stat(project):
    stat = count_project(project)
    label = str(project).upper()
    print(label)
    pprint.pprint(stat)


def calc_project(project):
    gitproj = Git(project)
    source_names = ls_files(gitproj, "*.[ch]")
    sourcedb = dict.fromkeys(source_names)
    for name in sourcedb:
        sourcedb[name] = {"path": Path(gitproj.working_dir) / name}
    for name, info in sourcedb.items():
        sourcedb[name]["line_count"] = line_count(info["path"])

    total_lines = sum([info["line_count"] for info in sourcedb.values()])
    return dict(
        gitproj=gitproj,
        sourcedb=sourcedb,
        total_lines=total_lines,
    )


def cmd_render(project):

    info = calc_project(project)
    sourcedb = info["sourcedb"]

    img = Image.new("RGB", [1000] * 2, (88, 88, 88))

    scale_x = img.width / info["total_lines"]
    draw = ImageDraw.Draw(img)

    cursor = 0
    labels = []
    important_width = img.width * 0.04

    for i, name in enumerate(sourcedb):
        info = sourcedb[name]
        width = scale_x * info["line_count"]
        color = PALETTE[i % len(PALETTE)]

        if width > important_width:
            print(name)
            labels.append(dict(x=cursor + 3, y=20, text=name))

        draw.rectangle(
            [cursor, 0, cursor + width, img.height],
            fill=color,
            # outline="gainsboro",
            # width=2,
        )
        cursor += width

    for label in labels:
        draw.text([label["x"], label["y"]], label["text"], fill="white")

    img.save("z.png", "PNG")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stat", dest="cmd", action="store_const", const=cmd_stat)
    parser.add_argument(
        "projects", nargs="+", type=Path, help="Git directory for project"
    )
    args = parser.parse_args()
    cmd = args.cmd or cmd_render
    cmd(project=args.projects[0])


if __name__ == "__main__":
    main()