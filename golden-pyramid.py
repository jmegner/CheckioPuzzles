def count_gold(pyr):
    bestCounts = [[0] * len(pyr) for row in pyr]

    for r, row in reversed(list(enumerate(pyr))):
        for c, num in enumerate(row):
            if r == len(pyr) - 1:
                bestCounts[r][c] = num
            else:
                bestCounts[r][c] = num + max(
                    bestCounts[r + 1][c], bestCounts[r + 1][c + 1])

    return bestCounts[0][0]


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert count_gold((
        (1,),
        (2, 3),
        (3, 3, 1),
        (3, 1, 5, 4),
        (3, 1, 3, 1, 3),
        (2, 2, 2, 2, 2, 2),
        (5, 6, 4, 5, 6, 4, 3)
    )) == 23, "First example"
    assert count_gold((
        (1,),
        (2, 1),
        (1, 2, 1),
        (1, 2, 1, 1),
        (1, 2, 1, 1, 1),
        (1, 2, 1, 1, 1, 1),
        (1, 2, 1, 1, 1, 1, 9)
    )) == 15, "Second example"
    assert count_gold((
        (9,),
        (2, 2),
        (3, 3, 3),
        (4, 4, 4, 4)
    )) == 18, "Third example"
