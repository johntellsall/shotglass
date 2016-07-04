# app/utils.py

def make_step_iter(step, max_):
    num = 0
    while True:
        yield num
        num = (num + step) % max_
