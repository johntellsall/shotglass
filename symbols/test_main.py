"test main -- outer-level commands"

from click.testing import CliRunner

import main
from state import query1, queryall

FLASK_DIR = "../SOURCE/flask/src/flask"
SAMPLE = "sample_code/test_code.py"


def test_ls_tags():
    "test list Git tags in project"
    runner = CliRunner()
    result = runner.invoke(main.ls_tags, [FLASK_DIR])
    assert result.exit_code == 0
    assert "'0.10.1'," in result.output

def test_main_interesting():
    con = main.raw_add_project('../SOURCE/flask', is_testing=True, only_interesting=True)
    print('interesting file count: ', query1(con, table='file'))
    con = main.raw_add_project('../SOURCE/flask', is_testing=True, only_interesting=False)
    print('full file count: ', query1(con, table='file'))

def test_main_add_project():
    con = main.raw_add_project('../SOURCE/flask', is_testing=True, only_interesting=True)
    first_symbol_query = '''
        select s.name, f.path 
        from symbol s, file f 
        where s.file_id = f.id
        limit 1
'''
    result = queryall(con, first_symbol_query)
    # "boring" aka not interesting result:
    # assert dict(result[0]) == {'name': 'author', 'path': 'docs/conf.py'}
    assert dict(result[0]) == {'name': 'Blueprint', 'path': 'src/flask/__init__.py'}

def test_ctags():
    "test list Ctags e.g. symbol/function information"
    runner = CliRunner()
    result = runner.invoke(main.ctags, [SAMPLE])
    assert result.exit_code == 0
    assert "'kind': 'function'," in result.output
