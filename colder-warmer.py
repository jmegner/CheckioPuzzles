import math
import collections
import itertools


g_farther = -1
g_sameDist = 0
g_closer = 1
g_gridLen = 10


class Loc(collections.namedtuple('Loc', ['r', 'c'])):

    def euclidDist(self, other):
        return math.hypot(self.r - other.r, self.c - other.c)


def checkio(steps):
    potentialLocs = set(
        [Loc(r,c) for (r, c) in itertools.product(range(g_gridLen), repeat=2)])

    currLoc = Loc(steps[0][0], steps[0][1])

    for currStep, prevStep in zip(steps[1:], steps[:-1]):
        currLoc = Loc(currStep[0], currStep[1])
        prevLoc = Loc(prevStep[0], prevStep[1])
        distChange = currStep[2]

        prunePotentialLocs(potentialLocs, prevLoc, currLoc, distChange, True)

    return locThatGivesMostInformationInWorstCase(potentialLocs, currLoc)


def prunePotentialLocs(
        potentialLocs, prevLoc, currLoc, distChange, doModify
    ):

    numPrunes = 0

    for goalLoc in list(potentialLocs):
        if getDistChangeType(prevLoc, currLoc, goalLoc) != distChange:
            numPrunes += 1
            if doModify:
                potentialLocs.remove(goalLoc)

    return numPrunes


def getDistChangeType(prevLoc, currLoc, goalLoc):
    currDist = currLoc.euclidDist(goalLoc)
    prevDist = prevLoc.euclidDist(goalLoc)
    return signum(prevDist - currDist)


def signum(num):
    if num > 0:
        return 1
    if num < 0:
        return -1
    return 0


def locThatGivesMostInformationInWorstCase(potentialLocs, currLoc):
    return max(potentialLocs, key = lambda loc:
        worstInformationGain(potentialLocs, currLoc, loc))


def worstInformationGain(potentialLocs, currLoc, nextLoc):
    return min([
        prunePotentialLocs(
            potentialLocs, currLoc, nextLoc, distChange, False)
        for distChange in [g_closer, g_sameDist, g_farther]])


if __name__ == '__main__':
    # This part is using only for self-checking and not necessary for
    # auto-testing
    from math import hypot
    MAX_STEP = 12

    def check_solution(func, goal, start):
        prev_steps = [start]

        for step in range(MAX_STEP):
            row, col = func([s[:] for s in prev_steps])

            if [row, col] == goal:
                return True

            if 10 <= row or 0 > row or 10 <= col or 0 > col:
                print("You gave wrong coordinates.")
                return False

            prev_distance = hypot(
                prev_steps[-1][0] - goal[0], prev_steps[-1][1] - goal[1])

            distance = hypot(row - goal[0], col - goal[1])

            alteration = 0 if prev_distance == distance else (
                1 if prev_distance > distance else -1)

            prev_steps.append([row, col, alteration])

        print("Too many steps")
        return False

    assert check_solution(checkio, [7, 7], [5, 5, 0]), "1st example"
    assert check_solution(checkio, [5, 6], [0, 0, 0]), "2nd example"

