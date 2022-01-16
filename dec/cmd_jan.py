import git


def is_major_flask(tag):
    return tag.name in ["1.0", "2.0.0"]


def cmd_jan(project_path):

    repo = git.Repo(project_path)
    release_tags = filter(is_major_flask, repo.tags)
    names = [t.name for t in release_tags]
    assert len(names) > 1
    print("okay")
