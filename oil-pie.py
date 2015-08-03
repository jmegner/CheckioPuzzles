'''
author: Jacob Egner
date: 2015-08-02
island: ice base

puzzle URLs:
http://www.checkio.org/mission/oil-pie/
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-oil-pie

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles
'''

from fractions import Fraction


def divide_pie(groupSizes):
    totalGroupSize = sum(abs(groupSize) for groupSize in groupSizes)
    remainingPie = Fraction(1)

    for groupSize in groupSizes:
        if groupSize > 0:
            remainingPie -= Fraction(groupSize, totalGroupSize)
        else:
            remainingPie *= 1 + Fraction(groupSize, totalGroupSize)

    return remainingPie.numerator, remainingPie.denominator


if __name__ == '__main__':
    assert isinstance((2, -2), (tuple, list)), "Return tuple or list"
    assert tuple(divide_pie((2, -1, 3))) == (1, 18), "Example"
    assert tuple(divide_pie((1, 2, 3))) == (0, 1), "All know about the pie"
    assert tuple(divide_pie((-1, -1, -1))) == (8, 27), "One by one"
    assert tuple(divide_pie((10,))) == (0, 1), "All together"

