'''
author: Jacob Egner
date: 2015-08-02
island: ice base

puzzle URLs:
http://www.checkio.org/mission/counting-tiles/solve/
https://github.com/Bryukh-Checkio-Tasks/checkio-task-counting-tiles

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

Note: you could iterator over one octant and one diagonal instead, but the
performance gain is not worth the complexity increase for this application
'''


import math


def checkio(radius):
    numWholeTiles = 0
    numPartialTiles = 0
    radiusSq = radius ** 2

    for r in range(math.ceil(radius)):
        for c in range(math.ceil(math.sqrt(radiusSq - r ** 2))):
            if r ** 2 + c ** 2 < radiusSq:
                if (r + 1) ** 2 + (c + 1) ** 2 <= radiusSq:
                    numWholeTiles += 1
                else:
                    numPartialTiles += 1

    return [numWholeTiles * 4, numPartialTiles * 4]


if __name__ == '__main__':
    assert checkio(2) == [4, 12], "N=2"
    assert checkio(3) == [16, 20], "N=3"
    assert checkio(2.1) == [4, 20], "N=2.1"
    assert checkio(2.5) == [12, 20], "N=2.5"

