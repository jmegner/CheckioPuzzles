'''
author: Jacob Egner
date: 2015-06-27 (update on 2015-07-29)
island: home

puzzle URLs:
http://www.checkio.org/mission/pawn-brotherhood/
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-pawn-brotherhood

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


def safe_pawns(pawnLocStrs):
    pawnLocs = set()

    for pawnLocStr in pawnLocStrs:
        r = ord(pawnLocStr[1]) - ord('1')
        c = ord(pawnLocStr[0]) - ord('a')
        pawnLocs.add((r, c))

    numSafePawns = 0

    for r, c in pawnLocs:
        if (r - 1, c - 1) in pawnLocs or (r - 1, c + 1) in pawnLocs:
            numSafePawns += 1

    return numSafePawns


if __name__ == '__main__':
    assert safe_pawns({"b4", "d4", "f4", "c3", "e3", "g5", "d2"}) == 6
    assert safe_pawns({"b4", "c4", "d4", "e4", "f4", "g4", "e5"}) == 1


