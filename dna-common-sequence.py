import itertools


#class Loc(collections.namedtuple('Loc', ['r', 'c'])): pass


def common(word1, word2):
    # rows for word1; columns for word2;
    numR = len(word1)
    numC = len(word2)
    seqsGrid = [[None] * numC for char in word1]

    for r,c in itertools.product(range(numR), range(numC)):
        if word1[r] == word2[c]:
            prevSequences = safeGet(seqsGrid, r - 1, c - 1)
            newSeqs = set([seq + word1[r] for seq in prevSequences])
        else:
            leftSeqs = safeGet(seqsGrid, r, c - 1)
            upSeqs = safeGet(seqsGrid, r - 1, c)

            leftSeqLen = len(next(iter(leftSeqs)))
            upSeqLen = len(next(iter(upSeqs)))

            if leftSeqLen > upSeqLen:
                newSeqs = leftSeqs
            elif leftSeqLen < upSeqLen:
                newSeqs = upSeqs
            else:
                newSeqs = leftSeqs | upSeqs;

        seqsGrid[r][c] = newSeqs

    bestSeqs = ','.join(sorted(seqsGrid[-1][-1]))
    return bestSeqs


def safeGet(grid, r, c):
    if(r < 0 or c < 0 or r >= len(grid) or c >= len(grid[r])
            or grid[r][c] is None):
        return set([""])

    return grid[r][c]


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for
    # auto-testing
    assert common("ACGTC", "TTACTC") == "ACTC", "One"
    assert common("CGCTA", "TACCG") == "CC,CG,TA", "Two"
    assert common("GCTT", "AAAAA") == "", "None"
