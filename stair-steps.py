'''
author: Jacob Egner
date: 2015-08-02
island: ice base

puzzle URLs:
http://www.checkio.org/mission/stair-steps/
https://github.com/Bryukh-Checkio-Tasks/checkio-task-stair-steps

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles
'''


def checkio(vals):
    vals = [0] + vals + [0]
    accums = vals.copy()

    for valIdx in range(2, len(vals)):
        accums[valIdx] += max(accums[valIdx - 1], accums[valIdx - 2])

    return accums[-1]


if __name__ == '__main__':
    assert checkio([5, -3, -1, 2]) == 6, 'Fifth'
    assert checkio([5, 6, -10, -7, 4]) == 8, 'First'
    assert checkio([-11, 69, 77, -51, 23, 67, 35, 27, -25, 95]) == 393, 'Second'
    assert checkio([-21, -23, -69, -67, 1, 41, 97, 49, 27]) == 125, 'Third'

