'''
author: Jacob Egner
date: 2015-08-06
island: ice base

puzzle URLs:
http://www.checkio.org/mission/cipher-crossword/
https://github.com/Bryukh-Checkio-Tasks/checkio-task-cipher-crossword

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

discussion:
Once again, my first solution was a recursive depth-first search.
Second solution is iterative via itertools.permutations and takes a flattened
approach to the grid.
'''


import itertools


################################################################################
# newer solution below;
#
# flattens the grid to simplify things;
# iterative, but tries EVERY permutation of words to lines until solved, so the
# solution is inefficient;
#

def checkio(clueGrid, allWords):
    # flatten clue grid into lines of full rows then full cols
    lineClues = clueGrid[::2]  + list(map(list, zip(*clueGrid)))[::2]

    # go through all orderings of words to lines
    for lineWords in itertools.permutations(map(list, allWords)):
        clueValToLetter = getConsistentClueValToLetter(lineWords, lineClues)

        # apply clue-to-letter mapping
        if clueValToLetter:
            answerGrid = [
                [clueValToLetter[clueVal] for clueVal in clueRow]
                for clueRow in clueGrid
            ]

            return answerGrid

    return None


def getConsistentClueValToLetter(lineWords, lineClues):
    clueValToLetter = {}
    letterToClueVal = {}

    for lineWord, lineClue in zip(lineWords, lineClues):
        for letter, clueVal in zip(lineWord, lineClue):
            if clueValToLetter.setdefault(clueVal, letter) != letter:
                return None
            if letterToClueVal.setdefault(letter, clueVal) != clueVal:
                return None

    clueValToLetter[0] = ' '
    return clueValToLetter


################################################################################
# older solution below;
#
# I COULD change the solution to flatten things, but I already have a flattened
# approach, and this solution is nice in that it keeps the natural structure
# of the problem;
#
# this solution find conflicts as early as possible, rather than fulling trying
# out a mapping of words to lines;
#
# perhaps one thing to improve is the final step of making the letter grid
#

def checkioOld(clueGrid, allWords):
    horizClues = clueGrid[::2]
    vertClues = list(map(list, zip(*clueGrid)))[::2]

    answerGrid = fillGrid(
        horizClues,
        vertClues,
        [],
        [],
        set(allWords),
    )

    return answerGrid


def fillGrid(
    horizClues,
    vertClues,
    horizWords,
    vertWords,
    remainingWords,
):
    if crosswordHasConflict(horizClues, vertClues, horizWords, vertWords):
        return None

    if(len(horizWords) == len(horizClues)
        and len(vertWords) == len(vertClues)
    ):
        return makeLetterGrid(horizWords, vertWords)

    horizWordAddMult = len(horizWords) <= len(vertWords)
    vertWordAddMult = not horizWordAddMult

    for word in sorted(remainingWords):
        result = fillGrid(
            horizClues,
            vertClues,
            horizWords + [word] * horizWordAddMult,
            vertWords + [word] * vertWordAddMult,
            remainingWords - set(word),
        )

        if result:
            return result

    return None


def crosswordHasConflict(
    horizClues,
    vertClues,
    horizWords,
    vertWords,
):
    lineClues = horizClues[:len(horizWords)] + vertClues[:len(vertWords)]
    clueValToLetter = {}
    letterToClueVal = {}

    for word, lineClue in zip(horizWords + vertWords, lineClues):
        for letter, clueVal in zip(word, lineClue):
            if clueValToLetter.setdefault(clueVal, letter) != letter:
                return True
            if letterToClueVal.setdefault(letter, clueVal) != clueVal:
                return True

    return False


def makeLetterGrid(horizWords, vertWords):
    letterGrid = []

    for r in range(2 * len(horizWords) - 1):
        if r % 2 == 0:
            letterGrid.append(list(horizWords[r // 2]))
        else:
            letterGrid.append([])

            for c in range(2 * len(vertWords) - 1):
                if c % 2 == 0:
                    letterGrid[-1].append(vertWords[c // 2][r])
                else:
                    letterGrid[-1].append(' ')

    return letterGrid


if __name__ == '__main__':
    assert checkio(
        [
            [21, 6, 25, 25, 17],
            [14, 0, 6, 0, 2],
            [1, 11, 16, 1, 17],
            [11, 0, 16, 0, 5],
            [26, 3, 14, 20, 6],
        ],
        ['hello', 'habit', 'lemma', 'ozone', 'bimbo', 'trace',]
        ) == [
            ['h', 'e', 'l', 'l', 'o'],
            ['a', ' ', 'e', ' ', 'z'],
            ['b', 'i', 'm', 'b', 'o'],
            ['i', ' ', 'm', ' ', 'n'],
            ['t', 'r', 'a', 'c', 'e'],
        ]

