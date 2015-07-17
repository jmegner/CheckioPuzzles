'''
author: Jacob Egner
date: 2015-07-15
island: mine

puzzle prompt:
http://www.checkio.org/mission/magic-square

puzzle prompt source repo:
https://github.com/Bryukh-Checkio-Tasks/checkio-task-magic-square

my checkio solution repo:
https://github.com/jmegner/CheckioPuzzles

'''


import copy
import itertools


def checkio(puzzleGrid):
    workGrid = copy.deepcopy(puzzleGrid)

    unusedVals = set(range(1, len(workGrid) ** 2 + 1))

    for r, c in itertools.product(range(len(workGrid)), repeat=2):
        unusedVals.discard(workGrid[r][c])

    depthFirstSearch(puzzleGrid, workGrid, unusedVals, 0)

    return workGrid


def depthFirstSearch(puzzleGrid, workGrid, unusedVals, pos):
    if gridHasViolation(workGrid):
        return False

    numVals = len(workGrid) ** 2

    if pos >= numVals:
        return True

    r, c = divmod(pos, len(workGrid))

    # if at a pre-given cell
    if puzzleGrid[r][c]:
        return depthFirstSearch(puzzleGrid, workGrid, unusedVals, pos + 1)

    for tryVal in sorted(list(unusedVals)):
        workGrid[r][c] = tryVal
        unusedVals.remove(tryVal)

        if depthFirstSearch(puzzleGrid, workGrid, unusedVals, pos + 1):
            return True

        workGrid[r][c] = 0
        unusedVals.add(tryVal)

    return False


def gridHasViolation(workGrid):
    sideLen = len(workGrid)
    numVals = sideLen * sideLen
    neededLineSum = (sideLen * (sideLen ** 2 + 1)) / 2

    for r in range(sideLen):
        if all(workGrid[r]) and sum(workGrid[r]) != neededLineSum:
            return True

    for c in range(sideLen):
        lineVals = [workGrid[r][c] for r in range(sideLen)]
        if all(lineVals) and sum(lineVals) != neededLineSum:
            return True

    diag1 = [workGrid[r][r] for r in range(sideLen)]

    if all(diag1) and sum(diag1) != neededLineSum:
        return True

    diag2 = [workGrid[r][sideLen - 1 - r] for r in range(sideLen)]

    if all(diag2) and sum(diag2) != neededLineSum:
        return True

    return False


if __name__ == '__main__':
    #This part is using only for self-testing.
    def check_solution(func, in_square):
        SIZE_ERROR = "Wrong size of the answer."
        MS_ERROR = "It's not a magic square."
        NORMAL_MS_ERROR = "It's not a normal magic square."
        NOT_BASED_ERROR = "Hm, this square is not based on given template."
        result = func(in_square)
        #check sizes
        N = len(result)
        if len(result) == N:
            for row in result:
                if len(row) != N:
                    print(SIZE_ERROR)
                    return False
        else:
            print(SIZE_ERROR)
            return False
        #check is it a magic square
        # line_sum = (N * (N ** 2 + 1)) / 2
        line_sum = sum(result[0])
        for row in result:
            if sum(row) != line_sum:
                print(MS_ERROR)
                return False
        for col in zip(*result):
            if sum(col) != line_sum:
                print(MS_ERROR)
                return False
        if sum([result[i][i] for i in range(N)]) != line_sum:
            print(MS_ERROR)
            return False
        if sum([result[i][N - i - 1] for i in range(N)]) != line_sum:
            print(MS_ERROR)
            return False

        #check is it normal ms
        good_set = set(range(1, N ** 2 + 1))
        user_set = set([result[i][j] for i in range(N) for j in range(N)])
        if good_set != user_set:
            print(NORMAL_MS_ERROR)
            return False
        #check it is the square based on input
        for i in range(N):
            for j in range(N):
                if in_square[i][j] and in_square[i][j] != result[i][j]:
                    print(NOT_BASED_ERROR)
                    return False
        return True


    assert check_solution(
        checkio,
        [
            [2, 7, 6],
            [9, 5, 1],
            [4, 3, 0],
        ]
    ), "1st example"

    assert check_solution(
        checkio,
        [
            [0, 0, 0],
            [0, 5, 0],
            [0, 0, 0],
        ]
    ), "2nd example"

    assert check_solution(
        checkio,
        [
            [1, 15, 14, 4],
            [12, 0, 0, 9],
            [8, 0, 0, 5],
            [13, 3, 2, 16],
        ]
    ), "3rd example"


