import itertools


# recursively try out next appropriate faces
def winning_die(enemyFaces, existingFaces = None):
    if existingFaces is None:
        existingFaces = []

    numRemainingFaces = len(enemyFaces) - len(existingFaces)
    remainingSum = sum(enemyFaces) - sum(existingFaces)

    if numRemainingFaces <= 1:
        if numRemainingFaces == 1:
            existingFaces.append(remainingSum)

        if dieIsFavorable(enemyFaces, existingFaces):
            return existingFaces
        else:
            return []

    prevFace = existingFaces[-1] if len(existingFaces) else 1

    # we must keep existingFaces sorted, so we start at prevFace; where we end
    # is determined by having enough spots for all the faces
    for nextFace in range(prevFace, remainingSum // numRemainingFaces + 1):
        thisDie = winning_die(enemyFaces, existingFaces + [nextFace])
        if thisDie:
            return thisDie

    return []


def dieIsFavorable(enemyFaces, ourFaces):
    winCount = 0
    loseCount = 0

    for enemyFace, ourFace in itertools.product(enemyFaces, ourFaces):
        winCount += ourFace > enemyFace
        loseCount += ourFace < enemyFace

    return winCount > loseCount


if __name__ == '__main__':
    #These are only used for self-checking and not necessary for auto-testing
    def check_solution(func, enemy):
        player = func(enemy)
        total = 0
        for p in player:
            for e in enemy:
                if p > e:
                    total += 1
                elif p < e:
                    total -= 1
        return total > 0

    assert check_solution(winning_die, [3, 3, 3, 3, 6, 6]), "Threes and Sixes"
    assert check_solution(winning_die, [4, 4, 4, 4, 4, 4]), "All Fours"
    assert check_solution(winning_die, [1, 1, 1, 4]), "Unities and Four"
    assert winning_die([1, 2, 3, 4, 5, 6]) == [], "All in row -- No die"
    '''
    assert winning_die([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == [], "big1"
    assert check_solution(winning_die,
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]), "big2"
    assert check_solution(winning_die,
        [1, 5, 5, 5, 5, 6, 6, 6, 6, 10]), "big3"
    assert check_solution(winning_die,
        [2, 4, 6, 8, 10, 12, 14, 16, 18]), "big4"
    '''

