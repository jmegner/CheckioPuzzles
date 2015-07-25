'''
author: Jacob Egner
date: 2015-07-25
island: electronic station

puzzle prompt:
http://www.checkio.org/mission/one-line-drawing/

puzzle prompt source repo:
https://github.com/Bryukh-Checkio-Tasks/checkio-task-radiation-search

my checkio solution repo:
https://github.com/jmegner/CheckioPuzzles

this puzzle is very similar to the calculate-islands puzzle from scientific
expedition island

'''


def checkio(partGrid):
    groupSizesAndTypes = []

    for r, row in enumerate(partGrid):
        for c, partType in enumerate(row):
            if partType:
                groupSize = touchAndGetSize(partGrid, partType, r, c)
                groupSizesAndTypes.append([groupSize, partType])

    biggestGroupSizeAndType = sorted(groupSizesAndTypes)[-1]
    return biggestGroupSizeAndType


def touchAndGetSize(partGrid, partType, r, c):
    if(r < 0 or c < 0
        or r >= len(partGrid) or c >= len(partGrid[r])
        or partGrid[r][c] != partType
    ):
        return 0

    partGrid[r][c] = 0
    groupSize = 1

    for rDel, cDel in ((0, -1), (0, +1), (-1, 0), (+1, 0)):
        groupSize += touchAndGetSize(partGrid, partType, r + rDel, c + cDel)

    return groupSize


#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio([
        [1, 2, 3, 4, 5],
        [1, 1, 1, 2, 3],
        [1, 1, 1, 2, 2],
        [1, 2, 2, 2, 1],
        [1, 1, 1, 1, 1]
    ]) == [14, 1], "14 of 1"

    assert checkio([
        [2, 1, 2, 2, 2, 4],
        [2, 5, 2, 2, 2, 2],
        [2, 5, 4, 2, 2, 2],
        [2, 5, 2, 2, 4, 2],
        [2, 4, 2, 2, 2, 2],
        [2, 2, 4, 4, 2, 2]
    ]) == [19, 2], '19 of 2'

