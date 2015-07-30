'''
author: Jacob Egner
date: 2015-07-29
island: scientific expedition

puzzle URLs:
http://www.checkio.org/mission/the-square-chest/
https://github.com/Bryukh-Checkio-Tasks/checkio-task-square-chest

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

keep track of horizontal-going-right and vertical-going-down segments in 2d
(r,c) coordinates; check for squares of various sizes at places that have both
a horizontal and vertical segment

'''


g_gridLen = 4


def checkio(segments):
    horizSegs = set()
    vertSegs = set()

    for segment in segments:
        addSegment(horizSegs, vertSegs, segment)

    numSquares = 0
    for r, c in horizSegs & vertSegs:
        for size in range(1, g_gridLen + 1):
            if hasSquare(horizSegs, vertSegs, r, c, size):
                numSquares += 1

    return numSquares


def addSegment(horizSegs, vertSegs, segment):
    segment = sorted(segment)
    r = (segment[0] - 1) // g_gridLen
    c = (segment[0] - 1) % g_gridLen

    if segment[1] - segment[0] == 1:
        horizSegs.add((r, c))
    else:
        vertSegs.add((r, c))


def hasSquare(horizSegs, vertSegs, r, c, size):
    for sideLen in range(size):
        if( (r, c + sideLen) not in horizSegs
            or (r + size, c + sideLen) not in horizSegs
            or (r + sideLen, c) not in vertSegs
            or (r + sideLen, c + size) not in vertSegs
        ):
            return False

    return True


if __name__ == '__main__':
    assert (checkio([
        [1, 2], [3, 4], [1, 5], [2, 6], [4, 8], [5, 6], [6, 7], [7, 8],
        [6, 10], [7, 11], [8, 12], [10, 11], [10, 14], [12, 16], [14, 15],
        [15, 16]
        ]) == 3), "First, from description"

    assert (checkio([
        [1, 2], [2, 3], [3, 4], [1, 5], [4, 8], [6, 7], [5, 9], [6, 10],
        [7, 11], [8, 12], [9, 13], [10, 11], [12, 16], [13, 14], [14, 15],
        [15, 16]
        ]) == 2), "Second, from description"

    assert (checkio([
        [1, 2], [1, 5], [2, 6], [5, 6]
        ]) == 1), "Third, one small square"

    assert (checkio([
        [1, 2], [1, 5], [2, 6], [5, 9], [6, 10], [9, 10]
        ]) == 0), "Fourth, it's not square"

    assert (checkio([
        [16, 15], [16, 12], [15, 11], [11, 10], [10, 14], [14, 13], [13, 9]
        ]) == 0), "Fifth, snake"

    assert (checkio([
        [16,15],[16,12],[15,11],[11,12],[11,10],[10,14],[9,10],[14,13],[13,9],
        [15,14],
        ]) == 3), "Test 7"


