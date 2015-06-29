def checkio(islandGrid):
    maxArea = 0
    for startR, row in enumerate(islandGrid):
        for startC, elem in enumerate(row):
            for endR in range(startR + 1, len(islandGrid) + 1):
                for endC in range(startC + 1, len(row) + 1):
                    if rectangleOkay(islandGrid, startR, startC, endR, endC):
                        maxArea = max(
                            maxArea,
                            (endR - startR) * (endC - startC))

    return maxArea


def rectangleOkay(islandGrid, startR, startC, endR, endC):
    okayLandTypes = 'GS'

    for r in range(startR, endR):
        for c in range(startC, endC):
            if islandGrid[r][c] not in okayLandTypes:
                return False

    return True


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert checkio(['G']) == 1, 'One cell - one variant'
    assert checkio(['GS',
                    'GS']) == 4, 'Four good cells'
    assert checkio(['GT',
                    'GG']) == 2, 'Four cells, but with a tree'
    assert checkio(['GGTGG',
                    'TGGGG',
                    'GSSGT',
                    'GGGGT',
                    'GWGGG',
                    'RGTRT',
                    'RTGWT',
                    'WTWGR']) == 9, 'Classic'
