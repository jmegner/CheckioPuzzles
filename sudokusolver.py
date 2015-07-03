import copy
import itertools


g_maxNum = 9
g_gridLen = 9


def checkio(puzzleGrid):
    workGrid = copy.deepcopy(puzzleGrid)

    # idx into grid as if 1d
    pos = 0
    numPos = g_gridLen ** 2

    def doBacktrack():
        nonlocal pos
        nonlocal workGrid
        nonlocal didBacktrack

        setAt(workGrid, pos, 0)
        pos -= 1

        # must backtrack over given cells
        while getAt(puzzleGrid, pos):
            pos -= 1

        didBacktrack = True

    while pos < numPos:
        didBacktrack = False

        # must skip over givens
        if getAt(puzzleGrid, pos):
            pos += 1
            continue

        # if we have backtracked to a pos where we have already tried every num
        if getAt(workGrid, pos) == g_maxNum:
            doBacktrack()

        # else there are numbers left to try at this pos
        else:
            incAt(workGrid, pos)

            while cellHasConflict(workGrid, pos):
                if getAt(workGrid, pos) == g_maxNum:
                    doBacktrack()
                    break

                incAt(workGrid, pos)

        if didBacktrack:
            if pos < 0:
                return puzzleGrid
        # else made progress
        else:
            pos += 1

    return workGrid


def incAt(grid, pos):
    setAt(grid, pos, getAt(grid, pos) + 1)


def getAt(grid, pos):
    if pos < 0:
        return 0

    r, c = divmod(pos, len(grid))
    return grid[r][c]


def setAt(grid, pos, val):
    r, c = divmod(pos, len(grid))
    grid[r][c] = val


def cellHasConflict(grid, pos):
    r, c = divmod(pos, len(grid))

    coordsToCheck = set(
        getRowCoords(r) + getColCoords(c) + getBlockCoords(r, c))

    coordsToCheck.remove((r, c))

    hasConflict = any([grid[r][c] == grid[r2][c2] for r2, c2 in coordsToCheck])
    return hasConflict


def getRowCoords(r):
    return [(r, c) for c in range(g_gridLen)]


def getColCoords(c):
    return [(r, c) for r in range(g_gridLen)]


def getBlockCoords(r, c):
    blockStartR = r // 3 * 3
    blockStartC = c // 3 * 3
    return list(itertools.product(
        range(blockStartR, blockStartR + 3),
        range(blockStartC, blockStartC + 3)))


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert checkio([
        [0, 7, 1, 6, 8, 4, 0, 0, 0],
        [0, 4, 9, 7, 0, 0, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 5, 0, 4],
        [0, 0, 0, 3, 0, 7, 0, 0, 0],
        [2, 0, 3, 0, 0, 0, 0, 9, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 9],
        [0, 0, 0, 0, 0, 3, 7, 2, 0],
        [0, 0, 0, 4, 9, 8, 6, 1, 0]]
        ) == [
        [3, 7, 1, 6, 8, 4, 9, 5, 2],
        [8, 4, 9, 7, 2, 5, 3, 6, 1],
        [5, 6, 2, 9, 3, 1, 4, 7, 8],
        [6, 8, 7, 2, 1, 9, 5, 3, 4],
        [9, 1, 4, 3, 5, 7, 2, 8, 6],
        [2, 5, 3, 8, 4, 6, 1, 9, 7],
        [1, 3, 6, 5, 7, 2, 8, 4, 9],
        [4, 9, 8, 1, 6, 3, 7, 2, 5],
        [7, 2, 5, 4, 9, 8, 6, 1, 3]], "first"

    assert checkio([
        [5, 0, 0, 7, 1, 9, 0, 0, 4],
        [0, 0, 1, 0, 3, 0, 5, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 5, 9, 7, 2, 6, 4, 0],
        [0, 0, 0, 6, 0, 1, 0, 0, 0],
        [0, 2, 6, 3, 8, 5, 9, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 5, 0, 2, 0, 0],
        [8, 0, 0, 4, 9, 7, 0, 0, 6]]
        ) == [
        [5, 6, 8, 7, 1, 9, 3, 2, 4],
        [9, 7, 1, 2, 3, 4, 5, 6, 8],
        [2, 3, 4, 5, 6, 8, 7, 9, 1],
        [1, 8, 5, 9, 7, 2, 6, 4, 3],
        [3, 9, 7, 6, 4, 1, 8, 5, 2],
        [4, 2, 6, 3, 8, 5, 9, 1, 7],
        [6, 1, 9, 8, 2, 3, 4, 7, 5],
        [7, 4, 3, 1, 5, 6, 2, 8, 9],
        [8, 5, 2, 4, 9, 7, 1, 3, 6]], "second"
    print('Local tests done')

