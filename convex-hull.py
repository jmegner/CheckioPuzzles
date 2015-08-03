'''
author: Jacob Egner
date: 2015-08-02
island: ice base

puzzle URLs:
http://www.checkio.org/mission/convex-hull/
https://github.com/Bryukh-Checkio-Tasks/checkio-task-convex-hull

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

Discussion:
I use the approach described at
https://www.topcoder.com/community/data-science/data-science-tutorials/geometry-concepts-line-intersection-and-its-applications/#convexhull
'''


import collections
import math


class Point(collections.namedtuple('Point', ['x', 'y'])):

    def __neg__(self):
        return Point(-self.x, -self.y)


    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)


    def __mul__(self, scale):
        return Point(self.x * scale, self.y * scale)


    def __truediv__(self, scale):
        return Point(self.x / scale, self.y / scale)


    def distTo(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)


    @staticmethod
    def crossProduct(p1, p2, p3):
        del1 = p2 - p1
        del2 = p3 - p2
        return del1.x * del2.y - del1.y * del2.x


def checkio(coords):
    pointToOrigIdx = {
        Point(*coord) : coordIdx
        for coordIdx, coord in enumerate(coords)
    }

    hullPoints = [min(pointToOrigIdx)]
    unusedPoints = set(pointToOrigIdx)

    while len(hullPoints) == 1 or hullPoints[0] != hullPoints[-1]:
        nextHullPoint = None

        for point in unusedPoints:
            if point == hullPoints[-1]:
                continue

            shouldReplaceNextHullPoint = False

            if nextHullPoint is None:
                shouldReplaceNextHullPoint = True
            else:
                crossVal = Point.crossProduct(
                    nextHullPoint, hullPoints[-1], point)

                if crossVal < 0:
                    shouldReplaceNextHullPoint = True
                elif crossVal > 0:
                    shouldReplaceNextHullPoint = False
                else:
                    newDist = hullPoints[-1].distTo(point)
                    oldDist = hullPoints[-1].distTo(nextHullPoint)
                    shouldReplaceNextHullPoint = newDist < oldDist

            if shouldReplaceNextHullPoint:
                nextHullPoint = point

        hullPoints.append(nextHullPoint)
        unusedPoints.remove(nextHullPoint)

    return [pointToOrigIdx[hullPoint] for hullPoint in hullPoints[:-1]]


if __name__ == '__main__':
    assert checkio(
        [[7, 6], [8, 4], [7, 2], [3, 2], [1, 6], [1, 8], [4, 9]]
    ) == [4, 5, 6, 0, 1, 2, 3], "First example"

    assert checkio(
        [[3, 8], [1, 6], [6, 2], [7, 6], [5, 5], [8, 4], [6, 8]]
    ) == [1, 0, 6, 3, 5, 2], "Second example"

    assert checkio(
        [[7,4],[5,2],[4,7],[4,1],[3,6],[1,4]]
    ) == [5, 4, 2, 0, 1, 3], "Test 6 with collinearities"

