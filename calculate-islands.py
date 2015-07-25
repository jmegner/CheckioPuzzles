'''
author: Jacob Egner
date: 2015-06-25, or maybe a few days earlier
island: scientific expedition

puzzle prompt:
http://www.checkio.org/mission/calculate-islands/

puzzle prompt source repo:
https://github.com/Bryukh-Checkio-Tasks/checkio-task-calculate-islands

my checkio solution repo:
https://github.com/jmegner/CheckioPuzzles

this puzzle is very similar to the radiation-search puzzle from electronic
station island

'''


import itertools


def checkio(landGrid):
    touchGrid = [[False] * len(landGrid[0]) for row in landGrid]
    landSizes = []

    for r, row in enumerate(landGrid):
        for c, isLand in enumerate(row):
            if isLand and not touchGrid[r][c]:
                landSizes.append(touchAndGetSize(landGrid, touchGrid, r, c))

    return sorted(landSizes)


def touchAndGetSize(landGrid, touchGrid, r, c):
    if (r < 0 or c < 0 or r >= len(landGrid) or c >= len(landGrid[r])
            or touchGrid[r][c] or not landGrid[r][c]):
        return 0

    touchGrid[r][c] = True
    landSize = 1

    for r2, c2 in itertools.product(range(r - 1, r + 2), range(c - 1, c + 2)):
        landSize += touchAndGetSize(landGrid, touchGrid, r2, c2)

    return landSize


#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio([[0, 0, 0, 0, 0],
                    [0, 0, 1, 1, 0],
                    [0, 0, 0, 1, 0],
                    [0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0]]) == [1, 3], "1st example"
    assert checkio([[0, 0, 0, 0, 0],
                    [0, 0, 1, 1, 0],
                    [0, 0, 0, 1, 0],
                    [0, 1, 1, 0, 0]]) == [5], "2nd example"
    assert checkio([[0, 0, 0, 0, 0, 0],
                    [1, 0, 0, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0],
                    [0, 0, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0, 0]]) == [2, 3, 3, 4], "3rd example"

