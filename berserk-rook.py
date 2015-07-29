'''
author: Jacob Egner
date: 2015-07-29
island: scientific expedition

puzzle URLs:
http://www.checkio.org/mission/berserk-rook/
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-berserk-rook

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


import collections


class Loc(collections.namedtuple('Loc', ['r', 'c'])):

    def __add__(self, other):
        return Loc(self.r + other.r, self.c + other.c)


    def __mul__(self, scale):
        return Loc(self.r * scale, self.c * scale)


    def fromChessStr(chessStr):
        return Loc(ord(chessStr[1]) - ord('1'), ord(chessStr[0]) - ord('a'))


def berserk_rook(berserkerStr, enemyStrs):
    berserkLoc = Loc.fromChessStr(berserkerStr)
    enemyLocs = set(Loc.fromChessStr(enemyStr) for enemyStr in enemyStrs)

    numCaptures = getNumCapturesPossible(berserkLoc, enemyLocs)

    return numCaptures


def getNumCapturesPossible(berserkLoc, enemyLocs):
    if not enemyLocs:
        return 0

    maxNumCaptures = 0

    directions = [Loc(0, -1), Loc(0, +1), Loc(-1, 0), Loc(+1, 0)]

    for direction in directions:
        for moveLen in range(1, 9):
            moveLoc = berserkLoc + direction * moveLen

            if moveLoc in enemyLocs:
                numCaptures = 1 + getNumCapturesPossible(
                    moveLoc, enemyLocs - set([moveLoc]))

                maxNumCaptures = max(numCaptures, maxNumCaptures)
                break

    return maxNumCaptures


if __name__ == '__main__':
    assert berserk_rook(
        'd3',
        {'d6', 'b6', 'c8', 'g4', 'b8', 'g6'}
        ) == 5, "one path"

    assert berserk_rook(
        'a2',
        {'f6', 'f2', 'a6', 'f8', 'h8', 'h6'}
        ) == 6, "several paths"

    assert berserk_rook(
        'a2',
        {'f6', 'f8', 'f2', 'a6', 'h6'}
        ) == 4, "Don't jump through"


