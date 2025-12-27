import main

def test_db_add_releases():
    con = main.raw_add_project(
        "../SOURCE/flask", is_testing=True, only_interesting=True
    )
    # file_rows = queryall(con, sql='select * from file where path = "src/flask/app.py"')
    # item = dict(file_rows[0])
    # print('FILE:', item)
    # symbol_rows = queryall(con, sql='select * from symbol where path = "src/flask/app.py"')
    # item = dict(symbol_rows[0])
    # print('SYMBOL:', item)
