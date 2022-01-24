import git


def is_major_flask(tag):
    return tag.name in ["1.0", "2.0.0"]


def cmd_jan(project_path):

    repo = git.Repo(project_path)
    release_tags = list(filter(is_major_flask, repo.tags))
    names = [t.name for t in release_tags]
    assert len(names) > 1
    for tag in release_tags:
        print(f"TAG: {tag}")
        for blob in tag.commit.tree:
            assert blob.type == "blob", blob.type
            if not blob.path.endswith("rst"):
                continue
            print(f"{tag.name} {blob.path} {blob.hexsha[:6]}")
            print(f" - {blob.abspath}")
    print("okay")


if __name__ == "__main__":
    cmd_jan("../SOURCE/flask")
