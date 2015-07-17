'''
author: Jacob Egner
date: 2015-07-17
island: mine

puzzle prompt:
http://www.checkio.org/mission/lantern-river

puzzle prompt source repo:
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-lantern-river

my checkio solution repo:
https://github.com/jmegner/CheckioPuzzles

'''


import collections


gc_land = 'X'
gc_water = '.'


def lanterns_flow(riverGrid, timeOfLight):
    numR = len(riverGrid)
    numC = len(riverGrid[0])
    workGrid = [list(riverGrid[r]) for r in range(numR)]
    lightedWaterRcs = set()

    for c in range(numC):
        if workGrid[0][c] == gc_water:
            lightedWaterRcs |= processLantern(workGrid, c, timeOfLight)

    return len(lightedWaterRcs)


def processLantern(workGrid, startC, timeOfLight):
    numR = len(workGrid)
    numC = len(workGrid[0])
    lightedWaterRcs = set()

    lanternId = startC

    prevR = -1
    prevC = startC

    currR = 0
    currC = startC

    currTime = 0

    while True:
        workGrid[currR][currC] = lanternId

        if currTime == timeOfLight:
            lightedWaterRcs = getLightedWaterRcs(workGrid, currR, currC)

        # done if reached bottom
        if currR == numR - 1:
            break

        delR = currR - prevR
        delC = currC - prevC

        # try order: right, straight, left
        tryRs = [
            currR + delC,
            currR + delR,
            currR - delC,
        ]
        tryCs = [
            currC - delR,
            currC + delC,
            currC + delR,
        ]

        foundNextSpot = False

        for tryR, tryC in zip(tryRs, tryCs):
            if( inBounds(workGrid, tryR, tryC)
                and workGrid[tryR][tryC] == gc_water
            ):
                foundNextSpot = True

                prevR = currR
                prevC = currC
                currR = tryR
                currC = tryC
                currTime += 1

                break

        if not foundNextSpot:
            raise ValueError("could not find next lantern spot")

    return lightedWaterRcs


def inBounds(grid, r, c):
    return r >= 0 and c >= 0 and r < len(grid) and c < len(grid[r])


def getLightedWaterRcs(workGrid, r, c):
    lightedWaterRcs = set()

    for r2 in range(r - 1, r + 2):
        for c2 in range(c - 1, c + 2):
            if inBounds(workGrid, r2, c2) and workGrid[r2][c2] != gc_land:
                lightedWaterRcs.add((r2, c2))

    return lightedWaterRcs


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert lanterns_flow((
        "X....XXX",
        "X....XXX",
        "X....XXX",
        "X....XXX",
        "X....XXX",
        "X......X",
        "X......X",
        "X......X",
        "X......X",
        "XXX....X",
        ), 0) == 8, "Start"

    assert lanterns_flow((
        "X....XXX",
        "X....XXX",
        "X....XXX",
        "X....XXX",
        "X....XXX",
        "X......X",
        "X......X",
        "X......X",
        "X......X",
        "XXX....X",
        ), 7) == 18, "7th minute"

    assert lanterns_flow((
        "X....XXX",
        "X....XXX",
        "X....XXX",
        "X....XXX",
        "X....XXX",
        "X......X",
        "X......X",
        "X......X",
        "X......X",
        "XXX....X",
        ), 9) == 17, "9th minute"


