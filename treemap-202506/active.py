# active.py -- show files with many changes

import state

db = state.get_db()

res = state.query1(db, """
select count(*) from file
""")

assert 0, res

print([row for row in res])