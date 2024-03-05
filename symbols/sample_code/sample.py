def beer(num):
    return 2 * num


class Whiskey:
    def sip(self):
        pass


def outer1():
    def inner():
        pass


def outer2():
    def inner():
        pass


def main():
    a = beer(1)
    b = beer(2) + beer(3)
    print(a, b)
