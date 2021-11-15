from git import Repo


def list_releases():
    return ["beer"]


TEST_REPO_DIR = "/Users/johnmitchell/jsrc/shotglass/SOURCE/coreutils"


def test_list():
    def is_release(tag):
        return tag.name.startswith("v")

    repo = Repo(TEST_REPO_DIR)
    release_tags = filter(is_release, repo.tags)
    names = [t.name for t in release_tags]
    assert "v4.5.1" in names
    assert len(names) > 10


if __name__ == "__main__":
    print(list_releases())
