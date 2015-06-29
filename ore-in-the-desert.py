import collections
import math


g_gridSize = 10


class Loc(collections.namedtuple('Loc', ['r', 'c'])):

    def euclidDist(self, other):
        return math.sqrt((self.r - other.r) ** 2 + (self.c - other.c) ** 2)


def checkio(prevProbes):
    numPrevProbes = len(prevProbes)

    if numPrevProbes == 0:
        # start in north west corner
        return [0, 0]
    if numPrevProbes == 1:
        # go no more than range-dist south from previous probe
        return [min(prevProbes[-1][2], g_gridSize - 1), 0]
    elif numPrevProbes == 2:
        # go no more than range-dist east from previous probe
        return [prevProbes[-1][0], min(prevProbes[-1][2], g_gridSize - 1)]

    for r in range(g_gridSize):
        for c in range(g_gridSize):
            probeLocs = [Loc(probe[0], probe[1]) for probe in prevProbes]
            probeDists = [probe[2] for probe in prevProbes]

            oreLoc = Loc(r, c)
            oreDists = [round(oreLoc.euclidDist(probeLoc)) for probeLoc
                in probeLocs]

            distsMatch = [probeDists[i] == oreDists[i] for i
                in range(len(probeDists))]

            if all(distsMatch):
                return r, c

            # entire body of this loop could be replaced with this single
            # if-statement that is not friendly to understanding or debugging
            '''
            if all([round(Loc(r, c).euclidDist(Loc(probe[0], probe[1])))
                    == probe[2] for probe in prevProbes]):
                return r, c
            '''

    raise ValueError("could not find good ore loc")


if __name__ == '__main__':
    #This part is using only for self-testing.
    def check_solution(func, ore):
        recent_data = []
        for step in range(4):
            row, col = func([d[:] for d in recent_data])  # copy the list
            if row < 0 or row > 9 or col < 0 or col > 9:
                print("Where is our probe?")
                return False
            if (row, col) == ore:
                return True
            dist = round(((row - ore[0]) ** 2 + (col - ore[1]) ** 2) ** 0.5)
            recent_data.append([row, col, dist])
        print("It was the last probe.")
        return False

    assert check_solution(checkio, (1, 1)), "Example"
    assert check_solution(checkio, (9, 9)), "Bottom right"
    assert check_solution(checkio, (6, 6)), "Center"
