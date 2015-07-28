'''
author: Jacob Egner
date: 2015-07-28
island: scientific expedition

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

simple brute force over all possible assignments of weights into two loads

'''


import itertools


def checkio(weights):
    minWeightDiff = sum(weights)

    for loadIdxs in itertools.product((0,1), repeat=len(weights)):
        weightSums = [0, 0]

        for loadIdx, weight in zip(loadIdxs, weights):
            weightSums[loadIdx] += weight

        minWeightDiff = min(minWeightDiff, abs(weightSums[0] - weightSums[1]))

    return minWeightDiff


if __name__ == '__main__':
    assert checkio([10, 10]) == 0, "1st example"
    assert checkio([10]) == 10, "2nd example"
    assert checkio([5, 8, 13, 27, 14]) == 3, "3rd example"
    assert checkio([5, 5, 6, 5]) == 1, "4th example"
    assert checkio([12, 30, 30, 32, 42, 49]) == 9, "5th example"
    assert checkio([1, 1, 1, 3]) == 0, "6th example"


