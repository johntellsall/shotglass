import build


# TODO: match something on command's output
def test_cmd_index():
    assert 0, build.cmd_index(project_path="..", temporary=True)


# TODO: match something on command's output
def test_cmd_info():
    assert 0, build.cmd_info(project_path="..")


# def cmd_ctags(file_path):
# def cmd_releases(project_path):
# def cmd_show(project_path):
# def cmd_nov(project_path):
