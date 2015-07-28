'''
author: Jacob Egner
date: 2015-07-27
island: elementary

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


import functools


def checkio(number):
    return functools.reduce(
        lambda a, b: a * b,
        [int(digit) for digit in str(number) if int(digit)]
    )


if __name__ == '__main__':
    assert checkio(123405) == 120
    assert checkio(999) == 729
    assert checkio(1000) == 1
    assert checkio(1111) == 1
