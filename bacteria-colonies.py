def healthy(grid):
    bestRadius = 0
    bestR = 0
    bestC = 0

    for r, row in enumerate(grid):
        for c, elem in enumerate(row):
            radius = getHealthyRadius(grid, r, c)

            if radius > bestRadius:
                bestRadius = radius
                bestR = r
                bestC = c

    return (bestR, bestC)


def getHealthyRadius(grid, r, c):
    if not grid[r][c]:
        return 0

    radius = 1

    while True:
        hopefullyFullRing = getRingCells(grid, r, c, radius)
        if not all(hopefullyFullRing):
            break

        radius += 1

    hopefullyEmptyRing = getRingCells(grid, r, c, radius)

    if any(hopefullyEmptyRing):
        return 0

    return radius


def getRingCells(grid, r, c, radius):
    ringCoords = set()

    for delR in range(radius + 1):
        delC = radius - delR

        ringCoords.add( (r + delR, c + delC) )
        ringCoords.add( (r + delR, c - delC) )
        ringCoords.add( (r - delR, c + delC) )
        ringCoords.add( (r - delR, c - delC) )

    ringCells = [grid[r2][c2] for r2, c2 in ringCoords
        if inBounds(grid, r2, c2)]

    return ringCells


def inBounds(grid, r, c):
    return r >= 0 and c >= 0 and r < len(grid) and c < len(grid[r])


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    def check(result, answers):
        return list(result) in answers

    check(healthy(((0, 1, 0),
                   (1, 1, 1),
                   (0, 1, 0),)), [[1, 1]])
    check(healthy(((0, 0, 1, 0, 0),
                   (0, 1, 1, 1, 0),
                   (0, 0, 1, 0, 0),
                   (0, 0, 0, 0, 0),
                   (0, 0, 1, 0, 0),)), [[1, 2]])
    check(healthy(((0, 0, 1, 0, 0),
                   (0, 1, 1, 1, 0),
                   (0, 0, 1, 0, 0),
                   (0, 0, 1, 0, 0),
                   (0, 0, 1, 0, 0),)), [[0, 0]])
    check(healthy(((0, 0, 0, 0, 0, 0, 1, 0),
                   (0, 0, 1, 0, 0, 1, 1, 1),
                   (0, 1, 1, 1, 0, 0, 1, 0),
                   (1, 1, 1, 1, 1, 0, 0, 0),
                   (0, 1, 1, 1, 0, 0, 1, 0),
                   (0, 0, 1, 0, 0, 1, 1, 1),
                   (0, 0, 0, 0, 0, 0, 1, 0),)), [[3, 2]])
    check(healthy(((0, 0, 0, 0, 0, 0, 2, 0),
                   (0, 0, 0, 2, 2, 2, 2, 2),
                   (0, 0, 1, 0, 0, 0, 2, 0),
                   (0, 1, 1, 1, 0, 0, 2, 0),
                   (1, 1, 1, 1, 1, 0, 2, 0),
                   (0, 1, 1, 1, 0, 0, 2, 0),
                   (0, 0, 1, 0, 0, 0, 2, 0),
                   (0, 0, 0, 1, 0, 0, 2, 0),
                   (0, 0, 1, 1, 1, 0, 2, 0),
                   (0, 1, 1, 1, 1, 1, 0, 0),
                   (0, 0, 1, 1, 1, 0, 0, 0),
                   (0, 0, 0, 1, 0, 0, 0, 0),)), [[4, 2], [9, 3]])
