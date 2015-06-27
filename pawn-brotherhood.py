def safe_pawns(pawnLocStrs):
    boardLen = 8
    pawnGrid = [[False] * boardLen for r in range(boardLen)]

    for pawnLocStr in pawnLocStrs:
        r = ord(pawnLocStr[1]) - ord('1')
        c = ord(pawnLocStr[0]) - ord('a')
        pawnGrid[r][c] = True

    numSafePawns = 0

    for r, row in list(enumerate(pawnGrid))[1:]:
        for c, isPawn in enumerate(row):
            if isPawn:
                protectedFromLeft = c > 0 and pawnGrid[r - 1][c - 1]
                protectedFromRight = c < boardLen - 1 and pawnGrid[r - 1][c + 1]

                if protectedFromLeft or protectedFromRight:
                    numSafePawns += 1

    return numSafePawns

if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert safe_pawns({"b4", "d4", "f4", "c3", "e3", "g5", "d2"}) == 6
    assert safe_pawns({"b4", "c4", "d4", "e4", "f4", "g4", "e5"}) == 1
