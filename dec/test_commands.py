import subprocess

import pytest

import build
import cmd_index


def test_cmd_index(capfd):
    build.cmd_index(project_path="..", temporary=True)

    captured = capfd.readouterr()
    assert "NUM SYMBOLS:" in captured.out


def test_cmd_info(capfd):
    build.cmd_info(project_path="..")

    captured = capfd.readouterr()
    assert "NUM FILES:" in captured.out


def test_cmd_ctags(capfd):
    cmd_index.cmd_ctags("shotlib.py")

    captured = capfd.readouterr()
    assert "'signature': '(temporary=False)'" in captured.out


def test_cmd_releases(capfd):
    build.cmd_releases("../SOURCE/flask/")

    captured = capfd.readouterr()
    assert "total files" in captured.out


def test_cmd_show(capfd):
    build.cmd_show(project_path="..")

    captured = capfd.readouterr()
    assert "source files" in captured.out


def test_commandline():
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.run("python3 ./build.py", shell=True, check=True)
