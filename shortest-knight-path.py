import itertools


g_boardLen = 8
g_maxDist = 1e99


def checkio(cells):
    beginR = ord(cells[1]) - ord('1')
    beginC = ord(cells[0]) - ord('a')
    endR = ord(cells[4]) - ord('1')
    endC = ord(cells[3]) - ord('a')

    stepsGrid = [[g_maxDist] * g_boardLen for row in range(g_boardLen)]
    stepsGrid[beginR][beginC] = 0

    thisStepLocs = set([(beginR, beginC)])
    nextStepLocs = set()

    numSteps = 0

    while stepsGrid[endR][endC] == g_maxDist:
        for r,c in thisStepLocs:

            rcDels = [
                [-2, -1],
                [-2, +1],
                [-1, -2],
                [-1, +2],
                [+2, -1],
                [+2, +1],
                [+1, -2],
                [+1, +2],
                ]

            for rDel, cDel in rcDels:
                r2 = r + rDel
                c2 = c + cDel

                if r2 < 0 or c2 < 0 or r2 >= g_boardLen or c2 >= g_boardLen:
                    continue

                if numSteps + 1 < stepsGrid[r2][c2]:
                    stepsGrid[r2][c2] = numSteps + 1
                    nextStepLocs.add((r2, c2))

        numSteps += 1
        thisStepLocs = nextStepLocs
        nextStepLocs = set()

    return numSteps


if __name__ == "__main__":
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert checkio("b1-d5") == 2, "1st example"
    assert checkio("a6-b8") == 1, "2nd example"
    assert checkio("h1-g2") == 4, "3rd example"
    assert checkio("h8-d7") == 3, "4th example"
    assert checkio("a1-h8") == 6, "5th example"
