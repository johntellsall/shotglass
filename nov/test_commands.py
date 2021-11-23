import subprocess

import pytest

import build
import cmd_index


def test_cmd_index(capfd):
    build.cmd_index(project_path="..", temporary=True)

    captured = capfd.readouterr()
    assert "CTAGS_ARGS" in captured.out


def test_cmd_info(capfd):
    build.cmd_info(project_path="..")

    captured = capfd.readouterr()
    assert "NUM FILES:" in captured.out


def test_cmd_ctags(capfd):
    cmd_index.cmd_ctags("shotlib.py")

    captured = capfd.readouterr()
    assert "'signature': '(temporary=False)'" in captured.out


# def cmd_releases(project_path):
# def cmd_nov(project_path):


@pytest.mark.xfail
def test_cmd_show(capfd):
    build.cmd_show(project_path="..")

    captured = capfd.readouterr()
    assert "NUM FILES:" in captured.out


def test_commandline(capfd):
    import pytest

    with pytest.raises(subprocess.CalledProcessError):
        subprocess.run("python3 ./build.py", shell=True, check=True)
