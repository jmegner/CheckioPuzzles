import collections
import math


class Loc(collections.namedtuple('Loc', ['r', 'c'])):

    def manhattanDist(self, other):
        return abs(self.r - other.r) + abs(self.c - other.c)


    def __add__(self, other):
        return Loc(self.r + other.r, self.c + other.c)


    def __mul__(self, scale):
        return Loc(self.r * scale, self.c * scale)


def find_distance(spiralPointId1, spiralPointId2):
    spiralPointLoc1 = getLoc(spiralPointId1)
    spiralPointLoc2 = getLoc(spiralPointId2)

    return spiralPointLoc1.manhattanDist(spiralPointLoc2)


def getLoc(spiralPointId):
    radius = math.ceil(math.sqrt(spiralPointId)) // 2
    sideLen = 2 * radius + 1
    oddSquare = sideLen ** 2

    cornerLocs = [
        Loc(-radius, -radius),  # top left
        Loc(+radius, -radius),  # bot left
        Loc(+radius, +radius),  # bot right
        Loc(-radius, +radius),] # top right

    cornerDels = [
        Loc( 1,  0),  # top left, going down
        Loc( 0,  1),  # bot left, going right
        Loc(-1,  0),  # bot right, going up
        Loc( 0, -1),] # top right, going left

    for sideIdx in range(4):
        cornerSpiralId = getCornerSpiralId(sideLen, sideIdx)
        nextCornerSpiralId = getCornerSpiralId(sideLen, sideIdx + 1)

        if spiralPointId >= nextCornerSpiralId:
            delSpiralId = cornerSpiralId - spiralPointId
            cornerLoc = cornerLocs[sideIdx]
            cornerDel = cornerDels[sideIdx]
            spiralPointLoc = cornerLoc + cornerDel * delSpiralId

            return spiralPointLoc

    return None


def getCornerSpiralId(sideLen, sideIdx):
    return sideLen ** 2 - sideIdx * (sideLen - 1)


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    print("in-file asserts begin")
    assert find_distance(1, 9) == 2, "First"
    assert find_distance(9, 1) == 2, "Reverse First"
    assert find_distance(10, 25) == 1, "Neighbours"
    assert find_distance(5, 9) == 4, "Diagonal"
    assert find_distance(26, 31) == 5, "One row"
    assert find_distance(50, 16) == 10, "One more test"
    print("in-file asserts end")

