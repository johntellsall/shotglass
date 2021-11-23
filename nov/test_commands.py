import pytest

import build


def test_cmd_index(capfd):
    build.cmd_index(project_path="..", temporary=True)

    captured = capfd.readouterr()
    assert "CTAGS_ARGS", captured.out


# TODO: match something on command's output
def test_cmd_info(capfd):
    build.cmd_info(project_path="..")

    captured = capfd.readouterr()
    assert "NUM FILES:" in captured.out


# def cmd_ctags(file_path):
# def cmd_releases(project_path):
# def cmd_show(project_path):
# def cmd_nov(project_path):
