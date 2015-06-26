import itertools


faceLeft = 0
faceRight = 1
faceOut = 2
numFaces = 3
numOrientations = 6

maxChips = 6

def checkio(chips):
    maxScore = 0
    attempts = 0
    canons = set()

    # try different locations for all but the first chip
    for permutedChips in itertools.permutations(chips[1:]):
        permutedChips = (chips[0],) + permutedChips

        if not chipsShareAFaceValue(permutedChips):
            continue

        canon = canonicalForm(permutedChips)

        if canon in canons:
            continue

        canons.add(canon)

        # try different orientations for all chips
        for orientCounts in itertools.product(
                range(numOrientations), repeat = len(chips)):

            orientedChips = tuple(map(
                chipOriented, permutedChips, orientCounts))

            if isLegal(orientedChips):
                score = sum([chip[faceOut] for chip in orientedChips])
                maxScore = max(maxScore, score)

            attempts += 1

    print("attempts " + str(attempts))

    return maxScore


def chipsShareAFaceValue(chips):
    for chipIdx, chip in enumerate(chips):
        nextChip = chips[(chipIdx + 1) % len(chips)]
        if set(chip).isdisjoint(set(nextChip)):
            return False

    return True


def isLegal(chips):
    for chipIdx, chip in enumerate(chips):
        nextChip = chips[(chipIdx + 1) % len(chips)]
        if chip[faceLeft] != nextChip[faceRight]:
            return False # was chipIdx

    return True # was len(chips)


def canonicalForm(chips):
    return tuple([tuple(sorted(chip)) for chip in chips])


def chipOriented(chip, orientCount):
    if orientCount == 0: return (chip[0], chip[1], chip[2])
    if orientCount == 1: return (chip[1], chip[2], chip[0])
    if orientCount == 2: return (chip[2], chip[0], chip[1])
    if orientCount == 3: return (chip[0], chip[2], chip[1])
    if orientCount == 4: return (chip[1], chip[0], chip[2])
    if orientCount == 5: return (chip[2], chip[1], chip[0])
    raise ValueError("bad orientCount")


#These "asserts" using only for self-checking and not necessary for auto-testing
def test():
    assert checkio(
        [[1, 1, 1], [1, 1, 1], [1, 1, 1],
         [1, 1, 1], [1, 1, 1], [1, 1, 1]]) == 6, "jme_00"
    assert checkio(
        [[1, 4, 20], [3, 1, 5], [50, 2, 3],
         [5, 2, 7], [7, 5, 20], [4, 7, 50]]) == 152, "First"
    assert checkio(
        [[1, 10, 2], [2, 20, 3], [3, 30, 4],
         [4, 40, 5], [5, 50, 6], [6, 60, 1]]) == 210, "Second"
    assert checkio(
        [[1, 2, 3], [2, 1, 3], [4, 5, 6],
         [6, 5, 4], [5, 1, 2], [6, 4, 3]]) == 21, "Third"
    assert checkio(
        [[5, 9, 5], [9, 6, 9], [6, 7, 6],
         [7, 8, 7], [8, 1, 8], [1, 2, 1]]) == 0, "Fourth"


if __name__ == '__main__':
    test()


