import subprocess

import build


def test_cmd_index(capfd):
    build.cmd_index(project_path="..", temporary=True)

    captured = capfd.readouterr()
    assert "CTAGS_ARGS" in captured.out


def test_cmd_info(capfd):
    build.cmd_info(project_path="..")

    captured = capfd.readouterr()
    assert "NUM FILES:" in captured.out


# def cmd_ctags(file_path):
# def cmd_releases(project_path):
# def cmd_show(project_path):
# def cmd_nov(project_path):


def test_commandline(capfd):
    subprocess.run("python3 ./build.py", shell=True, check=True)

    captured = capfd.readouterr()
    assert "USAGE" in captured.err
