class TrueComparer:

    trueCmp = lambda x, y: True
    __eq__ = trueCmp
    __ne__ = trueCmp
    __lt__ = trueCmp
    __le__ = trueCmp
    __gt__ = trueCmp
    __ge__ = trueCmp


def checkio(anything):
    return TrueComparer()


if __name__ == '__main__':
    import re
    import math

    assert checkio({}) != [],         'You'
    assert checkio('Hello') < 'World', 'will'
    assert checkio(80) > 81,           'never'
    assert checkio(re) >= re,          'make'
    assert checkio(re) <= math,        'this'
    assert checkio(5) == ord,          ':)'

    print('NO WAY :(')
