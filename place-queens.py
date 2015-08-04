'''
author: Jacob Egner
date: 2015-08-04
island: ice base

puzzle URLs:
http://www.checkio.org/mission/place-queens/
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-place-queens

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles
'''


import collections


g_boardSize = 8


class Loc(collections.namedtuple('Loc', ['r', 'c'])):

    @staticmethod
    def fromChessStr(chessStr):
        return Loc(ord(chessStr[1]) - ord('1'), ord(chessStr[0]) - ord('a'))


    def toChessStr(self):
        return chr(self.c + ord('a')) + chr(self.r + ord('1'))


    def posDiag(self):
        return self.r + self.c


    def negDiag(self):
        return self.r - self.c + g_boardSize - 1


    def hasQueenConflict(self, other):
        return( self.r == other.r or self.c == other.c
            or self.posDiag() == other.posDiag()
            or self.negDiag() == other.negDiag()
        )


################################################################################
# below is a fairly efficient solution, with simplicity sacrificed

def place_queens(givenQueenStrs):
    queens = [Loc.fromChessStr(queenStr) for queenStr in givenQueenStrs]

    rowCounts = [0] * g_boardSize
    colCounts = [0] * g_boardSize
    posDiagCounts = [0] * (2 * g_boardSize - 1)
    negDiagCounts = [0] * (2 * g_boardSize - 1)

    for queen in queens:
        rowCounts[queen.r] += 1
        colCounts[queen.c] += 1
        posDiagCounts[queen.posDiag()] += 1
        negDiagCounts[queen.negDiag()] += 1

    for count in rowCounts + colCounts + posDiagCounts + negDiagCounts:
        if count > 1:
            return set()

    tryMoreQueens(queens, rowCounts, colCounts, posDiagCounts, negDiagCounts)

    if len(queens) == g_boardSize:
        queenSet = set(queen.toChessStr() for queen in queens)
        return queenSet

    return set()


def tryMoreQueens(queens, rowCounts, colCounts, posDiagCounts, negDiagCounts):
    if len(queens) == g_boardSize:
        return True

    for r, rowCount in enumerate(rowCounts):
        if rowCount:
            continue

        for c, colCount in enumerate(colCounts):
            if colCount:
                continue

            tryLoc = Loc(r, c)
            posDiag = tryLoc.posDiag()
            negDiag = tryLoc.negDiag()

            if posDiagCounts[posDiag] or negDiagCounts[negDiag]:
                continue

            queens.append(tryLoc)
            rowCounts[r] += 1
            colCounts[c] += 1
            posDiagCounts[posDiag] += 1
            negDiagCounts[negDiag] += 1

            if(tryMoreQueens(
                queens, rowCounts, colCounts, posDiagCounts, negDiagCounts)
            ):
                return True

            queens.pop()
            rowCounts[r] -= 1
            colCounts[c] -= 1
            posDiagCounts[posDiag] -= 1
            negDiagCounts[negDiag] -= 1

    return False


################################################################################
# below is a very simple but fairly inefficient solution

def place_queens_simple(givenQueenStrs):
    givenQueens = [Loc.fromChessStr(queenStr) for queenStr in givenQueenStrs]

    for queen1Idx, queen1 in enumerate(givenQueens):
        for queen2 in givenQueens[queen1Idx + 1:]:
            if queen1.hasQueenConflict(queen2):
                return set()

    fullQueens = tryMoreQueensSimple(givenQueens)

    if len(fullQueens) == g_boardSize:
        queenSet = set(queen.toChessStr() for queen in fullQueens)
        return queenSet

    return set()


def tryMoreQueensSimple(queens):
    if len(queens) == g_boardSize:
        return queens

    for r in range(g_boardSize):
        for c in range(g_boardSize):
            tryLoc = Loc(r, c)
            locHasConflict = False

            for queen in queens:
                if tryLoc.hasQueenConflict(queen):
                    locHasConflict = True
                    break

            if not locHasConflict:
                fullQueens = tryMoreQueensSimple(queens + [tryLoc])
                if fullQueens:
                    return fullQueens

    return []


if __name__ == '__main__':
    from itertools import combinations
    COLS = "abcdefgh"
    ROWS = "12345678"

    THREATS = {c + r: set(
        [c + ROWS[k] for k in range(8)] +
        [COLS[k] + r for k in range(8)] +
        [COLS[k] + ROWS[i - j + k] for k in range(8) if 0 <= i - j + k < 8] +
        [COLS[k] + ROWS[- k + i + j] for k in range(8) if 0 <= - k + i + j < 8])
               for i, r in enumerate(ROWS) for j, c in enumerate(COLS)}

    def check_coordinate(coor):
        c, r = coor
        return c in COLS and r in ROWS

    def checker(func, placed, is_possible):
        user_set = func(placed.copy())
        if not all(isinstance(c, str) and len(c) == 2 and check_coordinate(c) for c in user_set):
            print("Wrong Coordinates")
            return False
        threats = []
        for f, s in combinations(user_set.union(placed), 2):
            if s in THREATS[f]:
                threats.append([f, s])
        if not is_possible:
            if user_set:
                print("Hm, how did you place them?")
                return False
            else:
                return True
        if not all(p in user_set for p in placed):
            print("You forgot about placed queens.")
            return False
        if is_possible and threats:
            print("I see some problems in this placement.")
            return False
        return True

    assert checker(place_queens, {"b2", "c4", "d6", "e8"}, True), "1st Example"
    assert checker(place_queens, {"b2", "c4", "d6", "e8", "a7", "g5"}, False), "2nd Example"
    assert checker(place_queens, {"a1", "h8"}, False), "Test Extra 2, conflict in givens"

