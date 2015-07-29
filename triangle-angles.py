'''
author: Jacob Egner
date: 2015-07-29
island: scientific expedition

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


import math


def checkio(*sideLens):
    resultForInvalid = [0, 0, 0]

    angles = []

    if 0 in sideLens:
        return resultForInvalid

    for sideIdx, sideLen0 in enumerate(sideLens):
        # calc angle corresponding to sideLen0

        sideLen1 = sideLens[(sideIdx + 1) % 3]
        sideLen2 = sideLens[(sideIdx + 2) % 3]

        if sideLen0 >= sideLen1 + sideLen2:
            return resultForInvalid

        lawOfCosinesVal = ((sideLen1 ** 2 + sideLen2 ** 2 - sideLen0 ** 2)
            / (2 * sideLen1 * sideLen2))

        if not (-1 <= lawOfCosinesVal <= +1):
            return resultForInvalid

        angles.append(round(math.degrees(math.acos(lawOfCosinesVal))))

    return sorted(angles)


if __name__ == '__main__':
    assert checkio(4, 4, 4) == [60, 60, 60], "All sides are equal"
    assert checkio(3, 4, 5) == [37, 53, 90], "Egyptian triangle"
    assert checkio(2, 2, 5) == [0, 0, 0], "It's can not be a triangle"


