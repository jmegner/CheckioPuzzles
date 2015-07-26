'''
author: Jacob Egner
date: 2015-07-17
island: electronic station

puzzle prompt:
http://www.checkio.org/mission/three-points-circle

puzzle prompt source repo:
https://github.com/Bryukh-Checkio-Tasks/checkio-task-three-points-circle

my checkio solution repo:
https://github.com/jmegner/CheckioPuzzles

overview:

first we realize that all are same radius from center point
(x1-a)^2+(y1-b)^2 = (x2-a)^2+(y2-b)^2 = (x3-a)^2+(y3-b)^2;

we reduce that quadratic triple equation into 2 linear equations (linear wrt
'a' and 'b');

(x2-x1)*a + (y2-y1)*b = (x2^2 + y2^2 - x1^2 - y1^2) / 2
(x3-x2)*a + (y3-y2)*b = (x3^2 + y3^2 - x2^2 - y2^2) / 2

then use Cramer's rule
https://en.wikipedia.org/wiki/Cramer%27s_rule

'''


import collections
import math

class Point(collections.namedtuple('Point', ['x', 'y'])):
    pass


def checkio(triplePointStr):
    pointStrs = triplePointStr.strip('()').split('),(')
    points = [Point(*map(float, pointStr.split(','))) for pointStr in pointStrs]

    ka = []
    kb = []
    kc = []

    for point1, point2 in zip(points[0:-1], points[1:]):
        ka.append(point2.x - point1.x)
        kb.append(point2.y - point1.y)
        kc.append(
            (point2.x ** 2 + point2.y ** 2 - point1.x ** 2 - point1.y ** 2)
            / 2)

    denom = ka[0] * kb[1] - kb[0] * ka[1]
    centerX = (kc[0] * kb[1] - kb[0] * kc[1]) / denom
    centerY = (ka[0] * kc[1] - kc[0] * ka[1]) / denom

    radius = math.sqrt(
        (points[0].x - centerX) ** 2
        + (points[0].y - centerY) ** 2)

    centerXStr = niceStr(-centerX)
    centerYStr = niceStr(-centerY)
    radiusStr = niceStr(radius)[1:]

    answerStr = ("(x" + centerXStr + ")^2+(y" + centerYStr
        + ")^2=" + radiusStr + "^2")

    return answerStr


def niceStr(value):
    return "{:+g}".format(round(value, 2))


#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio("(2,2),(6,2),(2,6)") == "(x-4)^2+(y-4)^2=2.83^2"
    assert checkio("(3,7),(6,9),(9,7)") == "(x-6)^2+(y-5.75)^2=3.25^2"


