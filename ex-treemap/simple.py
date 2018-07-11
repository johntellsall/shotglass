config = {'global': 1}


class Klass:
    def printme(self):
        print('me')


def double(num):
    return 2*num


def func():
    assert double(3) == 6


if __name__ == '__main__':
    func()
