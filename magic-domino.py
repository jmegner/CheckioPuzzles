'''
author: Jacob Egner
date: 2015-08-08
island: ice base

puzzle URLs:
http://www.checkio.org/mission/magic-domino/
https://github.com/pohmelie/checkio-task-magic-domino

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles
'''


import itertools


################################################################################
# new solution: based off of bunnychai's solution:
# http://www.checkio.org/mission/magic-domino/publications/bunnychai/python-3/fast-and-clean/
#
# note: a doubleRow usually refers to a list of dominos in a double row
# note: a rowPair usually refers to two rows of spot values

def magic_domino(goalSize, goalSum):
    colsOfGoalSum = allColsOfGoalSum(goalSize, goalSum)

    for disjointCols in collectionsOfDisjointGroups(colsOfGoalSum, goalSize):
        for doubleRows in collectionsOfGoodDoubleRowDominos(disjointCols, goalSize, goalSum):
            for rowPairs in collectionsOfGoodRowPairs(doubleRows, goalSum):
                for b in rearrangements(rowPairs):
                    if checkDiagonalSums(b, goalSum):
                        return list(zip(*b))


def allColsOfGoalSum(goalSize, goalSum):
    maxSpotVal = 6
    allDominos = [
        (spot1, spot2)
        for spot1 in range(maxSpotVal + 1)
        for spot2 in range(spot1, maxSpotVal + 1)
    ]

    colsOfGoalSum = []

    for colOfAnySum in itertools.combinations(allDominos, goalSize // 2):
        if sum(itertools.chain.from_iterable(colOfAnySum)) == goalSum:
            colsOfGoalSum.append(colOfAnySum)

    return colsOfGoalSum


def collectionsOfDisjointGroups(groups, numGroups, prevUsedDominos=set()):
    if numGroups == 0:
        yield []
    else:
        for firstGroupIdx, firstGroup in enumerate(groups):
            usedDominos = prevUsedDominos | set(firstGroup)

            groupsDisjointWithPrevGroups = [
                furtherGroup for furtherGroup in groups[firstGroupIdx + 1 :]
                if all(furtherElem not in usedDominos for furtherElem in furtherGroup)
            ]

            for disjointGroups in collectionsOfDisjointGroups(
                groupsDisjointWithPrevGroups, numGroups - 1, usedDominos
            ):
                yield [firstGroup] + disjointGroups


def collectionsOfGoodDoubleRowDominos(cols, goalSize, goalSum):
    goodDoubleRows = []

    # we generate double rows by choosing one domino from each col
    # a double row is a 1d list of dominos
    for doubleRow in itertools.product(*cols):
        if sum(itertools.chain.from_iterable(doubleRow)) == 2 * goalSum:
            goodDoubleRows.append(doubleRow)

    return collectionsOfDisjointGroups(goodDoubleRows, goalSize // 2)


# returns tuple:
#   first idx is double row
#   second idx is which of 2 rows within double row
#   third idx is spot val
def collectionsOfGoodRowPairs(doubleRows, goalSum):
    # list of list of dominos; each sublist is a double-row's worth of dominos
    # where each row is good
    veryGoodDoubleRows = []

    # doubleRow is 1d list of dominos
    for doubleRow in doubleRows:
        upperRowsSet = set()

        # go through all combos of two vals of each domino
        for rowSpotVals in itertools.product(*doubleRow):
            if sum(rowSpotVals) == goalSum:
                upperRowsSet.add(rowSpotVals)

        upperRows = list(upperRowsSet)
        lowerRows = [
            tuple(complementOfRowVals(doubleRow, upperRow))
            for upperRow in upperRows
        ]

        # the zip puts things back in domino form
        veryGoodDoubleRows.append(zip(upperRows, lowerRows))

    return itertools.product(*veryGoodDoubleRows)


def complementOfRowVals(doubleRow, rowVals):
    return (
        domino[0] if rowVals[dominoIdx] == domino[1] else domino[1]
        for dominoIdx, domino in enumerate(doubleRow)
    )


# permute over over double rows and cols
def rearrangements(rowPairs):
    # permute over double rows
    for rowPairsPermutation in itertools.permutations(rowPairs):
        rows = []

        for rowPair in rowPairsPermutation:
            rows.extend(rowPair)

        cols = zip(*rows)

        for colsPermutation in itertools.permutations(cols):
            yield colsPermutation


# check if diagonal sum is correct
def checkDiagonalSums(board, goalSum):
    size = len(board)
    return( sum(board[i][i] for i in range(size)) == goalSum
        and sum(board[i][size - 1 - i] for i in range(size)) == goalSum)


################################################################################
# solution old1: my original solution;
# very slow, basically depth-first recursive search trying one domino at a time

def magic_domino_old1(goalSize, goalSum):
    maxSpotVal = 6
    allDominos = set(
        (spot1, spot2)
        for spot1 in range(maxSpotVal + 1)
        for spot2 in range(spot1, maxSpotVal + 1)
    )

    spotGrid = recurse(goalSize, goalSum, [], allDominos)

    # we put each domino horizontally; desired format is each domino vertically
    if spotGrid:
        spotGrid = list(zip(*spotGrid))

    return spotGrid


def recurse(goalSize, goalSum, spotGrid, remainingDominos):
    if hasProblem(goalSize, goalSum, spotGrid, remainingDominos):
        return None

    if len(spotGrid) == goalSize and len(spotGrid[-1]) == goalSize:
        return spotGrid

    if not spotGrid or len(spotGrid[-1]) == goalSize:
        spotGrid.append([])

    rowSumRemaining = goalSum - sum(spotGrid[-1])
    rowLenRemaining = goalSize - len(spotGrid[-1])
    idealDominoSum = 2 * rowSumRemaining / rowLenRemaining

    dominoTryOrder = sorted(
        remainingDominos,
        key = lambda domino: abs(sum(domino) - idealDominoSum)
    )

    for unorientedDomino in dominoTryOrder:
        remainingDominos.remove(unorientedDomino)

        orientedDominos = sorted(set([
            unorientedDomino, tuple(reversed(unorientedDomino))]))

        for orientedDomino in orientedDominos:
            spotGrid[-1].extend(orientedDomino)

            result = recurse(goalSize, goalSum, spotGrid, remainingDominos)

            if result:
                return result

            spotGrid[-1].pop()
            spotGrid[-1].pop()

        remainingDominos.add(unorientedDomino)

    if not spotGrid[-1]:
        spotGrid.pop()

    return None


def hasProblem(goalSize, goalSum, spotGrid, remainingDominos):
    if not spotGrid:
        return False

    # check row sums
    for spotRow in spotGrid:
        rowSum = sum(spotRow)
        if len(spotRow) == goalSize and rowSum != goalSum or rowSum > goalSum:
            return True

    # check col sums
    for c in range(len(spotGrid[0])):
        colSum = getColSum(spotGrid, c)
        colIsFull = len(spotGrid) == goalSize and c < len(spotGrid[-1])

        if colIsFull and colSum != goalSum or colSum > goalSum:
            return True

    # check positive and negative diagonals

    posDiagSum = 0
    negDiagSum = 0

    for r, spotRow in enumerate(spotGrid):
        posC = r
        negC = goalSize - 1 - r

        if posC < len(spotGrid[r]):
            posDiagSum += spotGrid[r][posC]
        if negC < len(spotGrid[r]):
            negDiagSum += spotGrid[r][negC]

    if(len(spotGrid) == goalSize and len(spotGrid[-1]) == goalSize
        and posDiagSum != goalSum or posDiagSum > goalSum
    ):
        return True

    if(len(spotGrid) == goalSize and negDiagSum != goalSum
        or negDiagSum > goalSum
    ):
        return True

    if(goalSize > 4 and not canCompleteDoubleColumnsIndividually(
        goalSize, goalSum, spotGrid, remainingDominos)
    ):
        return True

    return False


def canCompleteDoubleColumnsIndividually(
    goalSize, goalSum, spotGrid, remainingDominos
):
    if not spotGrid:
        return True

    for colAIdx in range(0, goalSize, 2):
        colBIdx = colAIdx + 1

        colASumRemaining = goalSum - getColSum(spotGrid, colAIdx)
        colBSumRemaining = goalSum - getColSum(spotGrid, colBIdx)

        colLenRemaining = (goalSize - len(spotGrid)
            + (colAIdx >= len(spotGrid[-1]) - 1))

        if(not canCompleteDoubleColumn(
            colLenRemaining, colASumRemaining, colBSumRemaining,
            remainingDominos)
        ):
            return False

    return True


def canCompleteDoubleColumn(
    colLenRemaining,
    colASumRemaining,
    colBSumRemaining,
    remainingDominos,
):
    if colASumRemaining < 0 or colBSumRemaining < 0:
        return False

    if colLenRemaining == 0:
        return not colASumRemaining and not colBSumRemaining

    for unorientedDomino in sorted(remainingDominos):
        sortedSumsRemaining = sorted([colASumRemaining, colBSumRemaining])

        if(unorientedDomino[0] > sortedSumsRemaining[0]
            and unorientedDomino[1] > sortedSumsRemaining[1]
        ):
            break

        orientedDominos = sorted(set([
            unorientedDomino, tuple(reversed(unorientedDomino))]))

        for orientedDomino in orientedDominos:

            result = canCompleteDoubleColumn(
                colLenRemaining - 1,
                colASumRemaining - orientedDomino[0],
                colBSumRemaining - orientedDomino[1],
                remainingDominos - set([unorientedDomino]),
            )

            if result:
                return result

    return False


def getColSum(spotGrid, c):
    return sum(
        spotRow[c] for spotRow in spotGrid
        if c < len(spotRow)
    )


if __name__ == '__main__':
    import itertools

    def check_data(size, number, user_result):

        # check types
        check_container_type = lambda o: any(map(lambda t: isinstance(o, t), (list, tuple)))
        check_cell_type = lambda i: isinstance(i, int)
        if not (check_container_type(user_result) and
                all(map(check_container_type, user_result)) and
                all(map(lambda row: all(map(check_cell_type, row)), user_result))):
            raise Exception("You should return a list/tuple of lists/tuples with integers.")

        # check sizes
        check_size = lambda o: len(o) == size
        if not (check_size(user_result) and all(map(check_size, user_result))):
            raise Exception("Wrong size of answer.")

        # check is it a possible numbers (from 0 to 6 inclusive)
        if not all(map(lambda x: 0 <= x <= 6, itertools.chain.from_iterable(user_result))):
            raise Exception("Wrong matrix integers (can't be domino tiles)")

        # check is it a magic square
        seq_sum_check = lambda seq: sum(seq) == number
        diagonals_indexes = zip(*map(lambda i: ((i, i), (i, size - i - 1)), range(size)))
        values_from_indexes = lambda inds: itertools.starmap(lambda x, y: user_result[y][x], inds)
        if not (all(map(seq_sum_check, user_result)) and  # rows
                all(map(seq_sum_check, zip(*user_result))) and  # columns
                all(map(seq_sum_check, map(values_from_indexes, diagonals_indexes)))):  # diagonals
            raise Exception("It's not a magic square.")

        # check is it domino square
        tiles = set()
        for x, y in itertools.product(range(size), range(0, size, 2)):
            tile = tuple(sorted((user_result[y][x], user_result[y + 1][x])))
            if tile in tiles:
                raise Exception("It's not a domino magic square.")
            tiles.add(tile)

    size_and_sum_ranges = [
        [4, range(5, 20)],
        [6, range(13, 24)],
    ]

    import datetime
    print(datetime.datetime.now())

    for size, sum_range in size_and_sum_ranges:
        for desired_sum in sum_range:
            print("{}  size={} sum={}".format(
                datetime.datetime.now(), size, desired_sum))

            user_result = magic_domino(size, desired_sum)
            check_data(size, desired_sum, user_result)

    print(datetime.datetime.now())

