'''
author: Jacob Egner
date: 2015-08-02
island: ice base

puzzle URLs:
http://www.checkio.org/mission/shoot-range/
https://github.com/Bryukh-Checkio-Tasks/checkio-task-bullet-and-wall

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

Discussion:

My solution borrows from some line intersection code from my inside-block puzzle
solution.

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


class LineSegment:
    ''' implements line segment intersection algorithm as described at
    https://www.topcoder.com/community/data-science/data-science-tutorials/geometry-concepts-line-intersection-and-its-applications/
    '''

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.a = p2.y - p1.y
        self.b = p1.x - p2.x
        self.c = self.a * p1.x + self.b * p1.y


    def pointWithinBoundingBox(self, point):
        xs = [self.p1.x, self.p2.x]
        ys = [self.p1.y, self.p2.y]
        return (min(xs) <= point.x <= max(xs) and min(ys) <= point.y <= max(ys))


    def containsPoint(self, point):
        return (Point.crossProduct(self.p1, self.p2, point) == 0
            and self.pointWithinBoundingBox(point))


    def getIntersection(self, other):
        determinant = self.a * other.b - other.a * self.b

        if determinant == 0:
            return None
        else:
            lineIntersection = Point(
                (other.b * self.c - self.b * other.c) / determinant,
                (self.a * other.c - other.a * self.c) / determinant)

            intersectionIsOnBothSegments = (
                self.pointWithinBoundingBox(lineIntersection)
                and other.pointWithinBoundingBox(lineIntersection))

            if intersectionIsOnBothSegments:
                return lineIntersection

            return None


def shot(wall1, wall2, shotStart, shotLater):
    wall1 = Point(*wall1)
    wall2 = Point(*wall2)
    shotStart = Point(*shotStart)
    shotLater = Point(*shotLater)

    # make safe end of shot segment such that it is more than enough
    # to hit the wall
    laterDist = shotStart.distTo(shotLater)
    maxWallDist = max(shotStart.distTo(wall1), shotStart.distTo(wall2))
    safetyScaler = 2 * maxWallDist / laterDist
    shotEnd = shotStart + (shotLater - shotStart) * safetyScaler

    wallSegment = LineSegment(Point(*wall1), Point(*wall2))
    shotSegment = LineSegment(shotStart, shotEnd)

    intersection = wallSegment.getIntersection(shotSegment)

    if not intersection:
        return -1

    wallCenter = (wall1 + wall2) / 2
    wallHalfLen = wallCenter.distTo(wall2)

    score = 100 * (1 - intersection.distTo(wallCenter) / wallHalfLen)

    roundedScore = round(score)
    return roundedScore


if __name__ == '__main__':
    assert shot((2, 2), (5, 7), (11, 2), (8, 3)) == 100, "1st case"
    assert shot((2, 2), (5, 7), (11, 2), (7, 2)) == 0, "2nd case"
    assert shot((2, 2), (5, 7), (11, 2), (8, 4)) == 29, "3th case"
    assert shot((2, 2), (5, 7), (11, 2), (9, 5)) == -1, "4th case"
    assert shot((2, 2), (5, 7), (11, 2), (10.5, 3)) == -1, "4th case again"

