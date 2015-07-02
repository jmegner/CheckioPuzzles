def capture(matrix):
    numNodes = len(matrix)
    bestTimes = [1e99] * numNodes

    infectAdjacent(matrix, bestTimes, 0, 0)

    return max(bestTimes)


def infectAdjacent(matrix, bestTimes, nodeIdx, currTime):
    if currTime > bestTimes[nodeIdx]:
        return

    bestTimes[nodeIdx] = currTime

    for neighborIdx in range(len(matrix)):
        if neighborIdx != nodeIdx and matrix[nodeIdx][neighborIdx]:
            infectAdjacent(
                matrix, bestTimes, neighborIdx,
                currTime + matrix[neighborIdx][neighborIdx])


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert capture([[0, 1, 0, 1, 0, 1],
                    [1, 8, 1, 0, 0, 0],
                    [0, 1, 2, 0, 0, 1],
                    [1, 0, 0, 1, 1, 0],
                    [0, 0, 0, 1, 3, 1],
                    [1, 0, 1, 0, 1, 2]]) == 8, "Base example"
    assert capture([[0, 1, 0, 1, 0, 1],
                    [1, 1, 1, 0, 0, 0],
                    [0, 1, 2, 0, 0, 1],
                    [1, 0, 0, 1, 1, 0],
                    [0, 0, 0, 1, 3, 1],
                    [1, 0, 1, 0, 1, 2]]) == 4, "Low security"
    assert capture([[0, 1, 1],
                    [1, 9, 1],
                    [1, 1, 9]]) == 9, "Small"
