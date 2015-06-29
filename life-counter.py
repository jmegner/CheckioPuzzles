################################################################################
# new set/dict way

import collections


class Loc(collections.namedtuple('Loc', ['r', 'c'])):
    pass


def life_counter(initialGrid, numTicks):
    currLifeLocs = set([
        Loc(r, c)
        for r in range(len(initialGrid))
        for c in range(len(initialGrid[r]))
        if initialGrid[r][c]])

    for tick in range(numTicks):
        neighborCounts = collections.Counter()

        for liveCellLoc in currLifeLocs:
            neighborLocs = [
                Loc(liveCellLoc.r + delR, liveCellLoc.c + delC)
                for delR in range(-1, 2)
                for delC in range(-1, 2)
                if delR != 0 or delC != 0]

            neighborCounts.update(neighborLocs)

        nextLifeLocs = set()

        for loc, neighborCount in neighborCounts.items():
            if neighborCount == 2 and loc in currLifeLocs or neighborCount == 3:
                nextLifeLocs.add(loc)

        currLifeLocs = nextLifeLocs

    return len(currLifeLocs)


################################################################################
# old grid-based way

import itertools


def life_counter_old(initialGrid, numTicks):
    currGrid = [[cell for cell in row] for row in initialGrid]

    for tick in range(numTicks):
        currGrid = getMinimalGrid(currGrid)
        nextGrid = [[None] * len(currGrid[0]) for r in range(len(currGrid))]

        for r in range(len(nextGrid)):
            for c in range(len(nextGrid[r])):
                numLiveNeighbors = getNumLiveNeighbors(currGrid, r, c)

                if numLiveNeighbors == 2:
                    nextGrid[r][c] = getCell(currGrid, r, c)
                elif numLiveNeighbors == 3:
                    nextGrid[r][c] = 1
                else:
                    nextGrid[r][c] = 0

        currGrid = nextGrid

    numLiveCells = sum(itertools.chain(*currGrid))
    return numLiveCells


def getMinimalGrid(lifeGrid):
    numR = len(lifeGrid)
    numC = len(lifeGrid[0])
    minR = None
    maxR = None
    minC = None
    maxC = None

    for r in range(numR):
        if any(lifeGrid[r]):
            minR = r - 1
            break

    for r in reversed(range(numR)):
        if any(lifeGrid[r]):
            maxR = r + 1
            break

    for c, r in itertools.product(range(numC), range(numR)):
        if lifeGrid[r][c]:
            minC = c - 1
            break

    for c, r in itertools.product(reversed(range(numC)), range(numR)):
        if lifeGrid[r][c]:
            maxC = c + 1
            break

    if minR is None or (minR == 0 and minC == 0 and maxR == len(lifeGrid) - 1
            and maxC == len(lifeGrid[0]) - 1):
        return lifeGrid

    minimalGrid = [
        [getCell(lifeGrid, r, c)
        for c in range(minC, maxC + 1)]
        for r in range(minR, maxR + 1)]

    return minimalGrid


def getNumLiveNeighbors(lifeGrid, r, c):
    numLiveNeighbors = 0

    for r2 in range(r - 1, r + 2):
        for c2 in range(c - 1, c + 2):
            if getCell(lifeGrid, r2, c2) and (r != r2 or c != c2):
                numLiveNeighbors += 1

    return numLiveNeighbors


def getCell(lifeGrid, r, c):
    if inBounds(lifeGrid, r, c):
        return lifeGrid[r][c]
    return 0


def inBounds(grid, r, c):
    return r >= 0 and c >= 0 and r < len(grid) and c < len(grid[r])


################################################################################
# tests

if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    print("in-file asserts begin")
    assert life_counter(((0, 1, 0, 0, 0, 0, 0),
                         (0, 0, 1, 0, 0, 0, 0),
                         (1, 1, 1, 0, 0, 0, 0),
                         (0, 0, 0, 0, 0, 1, 1),
                         (0, 0, 0, 0, 0, 1, 1),
                         (0, 0, 0, 0, 0, 0, 0),
                         (1, 1, 1, 0, 0, 0, 0)), 4) == 15, "Example"
    assert life_counter(((0, 1, 0, 0, 0, 0, 0),
                         (0, 0, 1, 0, 0, 0, 0),
                         (1, 1, 1, 0, 0, 0, 0),
                         (0, 0, 0, 0, 0, 1, 1),
                         (0, 0, 0, 0, 0, 1, 1),
                         (0, 0, 0, 0, 0, 0, 0),
                         (1, 1, 1, 0, 0, 0, 0)), 15) == 14, "Little later"
    assert life_counter(((0, 1, 0),
                         (0, 0, 1),
                         (1, 1, 1)), 50) == 5, "Glider"
    assert life_counter(((1, 1, 0, 1, 1),
                         (1, 1, 0, 1, 1),
                         (0, 0, 0, 0, 0),
                         (1, 1, 0, 1, 1),
                         (1, 1, 0, 1, 1)), 100) == 16, "Stones"
    print("in-file asserts end")

