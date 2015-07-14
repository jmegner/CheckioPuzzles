'''
author: Jacob Egner
date: 2015-07-14
island: mine

puzzle prompt:
http://www.checkio.org/mission/matrix-pattern/

puzzle prompt source repo:
https://github.com/Bryukh-Checkio-Tasks/checkio-task-matrix-pattern

my checkio solution repo:
https://github.com/jmegner/CheckioPuzzles

'''

import itertools


def checkio(pattern, grid):
    endCheckR = len(grid) - len(pattern) + 1
    endCheckC = len(grid[0]) - len(pattern[0]) + 1

    for r, c in itertools.product(range(endCheckR), range(endCheckC)):
        checkAndMarkPattern(pattern, grid, r, c)

    return grid


def checkAndMarkPattern(pattern, grid, gridStartR, gridStartC):
    patternMatches = True
    rcItr1, rcItr2 = itertools.tee(
        itertools.product(range(len(pattern)), range(len(pattern[0]))),
        2)

    for r, c in rcItr1:
        if pattern[r][c] != grid[gridStartR + r][gridStartC + c]:
            patternMatches = False
            break

    if patternMatches:
        for r, c in rcItr2:
            grid[gridStartR + r][gridStartC + c] += 2

        return True

    return False


#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio(
        [[1, 0], [1, 1]],
        [
            [0, 1, 0, 1, 0],
            [0, 1, 1, 0, 0],
            [1, 0, 1, 1, 0],
            [1, 1, 0, 1, 1],
            [0, 1, 1, 0, 0],
        ]) == [
            [0, 3, 2, 1, 0],
            [0, 3, 3, 0, 0],
            [3, 2, 1, 3, 2],
            [3, 3, 0, 3, 3],
            [0, 1, 1, 0, 0],
        ]

    assert checkio(
        [[1, 1], [1, 1]],
        [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]) == [
            [3, 3, 1],
            [3, 3, 1],
            [1, 1, 1],
        ]

    assert checkio(
        [[0, 1, 0], [1, 1, 1]],
        [
            [0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 1, 1, 0, 1, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 1, 1],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 0, 0, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]) == [
            [0, 2, 3, 2, 0, 0, 0, 2, 3, 2],
            [0, 3, 3, 3, 0, 0, 0, 3, 3, 3],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 3, 2, 0, 0, 0],
            [2, 3, 2, 0, 3, 3, 3, 0, 1, 0],
            [3, 3, 3, 0, 0, 0, 0, 0, 1, 1],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 2, 3, 2, 0],
            [0, 1, 1, 0, 0, 0, 3, 3, 3, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]


