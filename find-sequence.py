'''
author: Jacob Egner
date: 2015-07-27
island: electronic station

puzzle prompt:
http://www.checkio.org/mission/find-sequence/

puzzle prompt source repo:
https://github.com/Bryukh-Checkio-Tasks/checkio-task-find-sequence

for latest version of my solution, see my checkio solution repo:
https://github.com/jmegner/CheckioPuzzles

'''


gc_sequenceLen = 4


def checkio(grid):
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if sequenceStartsHere(grid, r, c):
                return True

    return False


def sequenceStartsHere(grid, r, c):

    for horizMult, vertMult in ((1, 0), (0, 1), (1, 1), (-1, 1)):
        foundSequence = True

        for offset in range(gc_sequenceLen):
            r2 = r + offset * horizMult
            c2 = c + offset * vertMult

            if(r2 < 0 or c2 < 0
                or r2 >= len(grid) or c2 >= len(grid[r2])
                or grid[r][c] != grid[r2][c2]
            ):
                foundSequence = False
                break;

        if foundSequence:
            return True

    return False


if __name__ == '__main__':
    assert checkio([
        [1, 2, 1, 1],
        [1, 1, 4, 1],
        [1, 3, 1, 6],
        [1, 7, 2, 5]
    ]) == True, "Vertical"
    assert checkio([
        [7, 1, 4, 1],
        [1, 2, 5, 2],
        [3, 4, 1, 3],
        [1, 1, 8, 1]
    ]) == False, "Nothing here"
    assert checkio([
        [2, 1, 1, 6, 1],
        [1, 3, 2, 1, 1],
        [4, 1, 1, 3, 1],
        [5, 5, 5, 5, 5],
        [1, 1, 3, 1, 1]
    ]) == True, "Long Horizontal"
    assert checkio([
        [7, 1, 1, 8, 1, 1],
        [1, 1, 7, 3, 1, 5],
        [2, 3, 1, 2, 5, 1],
        [1, 1, 1, 5, 1, 4],
        [4, 6, 5, 1, 3, 1],
        [1, 1, 9, 1, 2, 1]
    ]) == True, "Diagonal"

