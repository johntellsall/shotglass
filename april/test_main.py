from click.testing import CliRunner
import main


# def test_hello_world():
#     runner = CliRunner()
#     result = runner.invoke(main.hello, ["Peter"])
#     assert result.exit_code == 0
#     assert result.output == "Hello Peter!\n"


def test_ctags():
    res = list(main.run_ctags("test_code.py"))
