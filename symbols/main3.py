import logging
import state


logging.basicConfig(format="%(asctime)-15s %(message)s", level=logging.INFO)

def main():
    db = state.get_db()
    symbols = state.queryall(db, sql="select * from symbol limit 10")
    assert 0, symbols

if __name__ == "__main__":
    main()