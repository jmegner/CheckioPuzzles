import collections


class Point(collections.namedtuple('Point', ['x', 'y'])):

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)


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


    def doesIntersect(self, other):
        determinant = self.a * other.b - other.a * self.b

        if determinant == 0:
            return False
        else:
            lineIntersection = Point(
                (other.b * self.c - self.b * other.c) / determinant,
                (self.a * other.c - other.a * self.c) / determinant)

            intersectionIsOnBothSegments = (
                self.pointWithinBoundingBox(lineIntersection)
                and other.pointWithinBoundingBox(lineIntersection))

            return intersectionIsOnBothSegments


def is_inside(polygon, queryXy):
    numIntersections = 0
    queryPoint = Point(*queryXy)
    queryRay = LineSegment(
        queryPoint,
        Point(-hash(queryPoint), -hash(tuple(polygon))))

    for pointIdx in range(len(polygon)):
        polygonPoint1 = Point(*polygon[pointIdx])
        polygonPoint2 = Point(*polygon[(pointIdx + 1) % len(polygon)])
        polygonSegment = LineSegment(polygonPoint1, polygonPoint2)

        if polygonSegment.containsPoint(queryPoint):
            return True

        if polygonSegment.doesIntersect(queryRay):
            numIntersections += 1

    return numIntersections % 2 == 1


if __name__ == '__main__':
    print("in-file asserts begin")
    assert is_inside(
        ((1, 1), (1, 3), (3, 3), (3, 1)),
        (2, 2)) == True, "First"
    assert is_inside(
        ((1, 1), (1, 3), (3, 3), (3, 1)),
        (4, 2)) == False, "Second"
    assert is_inside(
        ((1, 1), (4, 1), (2, 3)),
        (3, 2)) == True, "Third"
    assert is_inside(
        ((1, 1), (4, 1), (1, 3)),
        (3, 3)) == False, "Fourth"
    assert is_inside(
        ((2, 1), (4, 1), (5, 3), (3, 4), (1, 3)),
        (4, 3)) == True, "Fifth"
    assert is_inside(
        ((2, 1), (4, 1), (3, 2), (3, 4), (1, 3)),
        (4, 3)) == False, "Sixth"
    assert is_inside(
        ((1, 1), (3, 2), (5, 1), (4, 3), (5, 5), (3, 4), (1, 5), (2, 3)),
        (3, 3)) == True, "Seventh"
    assert is_inside(
        ((1, 1), (1, 5), (5, 5), (5, 4), (2, 4), (2, 2), (5, 2), (5, 1)),
        (4, 3)) == False, "Eighth"
    assert is_inside(
        ((1,1),(1,3),(2,4),(4,4),(4,3),(2,1)),
        (3,1)) == False, "from extra test 8"
    print("in-file asserts end")

