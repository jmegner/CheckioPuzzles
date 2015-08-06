'''
author: Jacob Egner
date: 2015-08-04
island: ice base

puzzle URLs:
http://www.checkio.org/mission/poker-dice/
https://github.com/MagiMaster/checkio-task-poker-dice

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

note: re-uses some code from texas-referee puzzle from electronic station
'''


import collections
import functools
import itertools
import random


g_highCards = "high cards"
g_onePair = "one pair"
g_twoPair = "two pair"
g_threeOfAKind = "three of a kind"
g_flush = "flush"
g_straight = "straight"
g_fullHouse = "full house"
g_fourOfAKind = "four of a kind"
g_fiveOfAKind = "five of a kind"

g_handTypeToScore = {
    g_highCards     : 0,
    g_onePair       : 2,
    g_twoPair       : 4,
    g_threeOfAKind  : 6,
    g_flush         : 15,
    g_straight      : 25,
    g_fullHouse     : 25,
    g_fourOfAKind   : 50,
    g_fiveOfAKind   : 200,
}

g_handTypeToAceBonus = {
    g_highCards     : 0,
    g_onePair       : 1,
    g_twoPair       : 1,
    g_threeOfAKind  : 2,
    g_flush         : 0,
    g_straight      : 0,
    g_fullHouse     : 5,
    g_fourOfAKind   : 10,
    g_fiveOfAKind   : 240,
}


class Card(collections.namedtuple("Card", ["rank", "suit"])):

    rankChars = "9TJQKA"
    suitChars = "SCDH"
    ranks = tuple(range(len(rankChars)))
    suits = tuple(range(len(suitChars)))
    aceRank = 14


    @staticmethod
    def fromStr(cardStr):
        return Card(
            Card.rankChars.index(cardStr[0]),
            Card.suitChars.index(cardStr[1]),
        )


    def __str__(self):
        return Card.rankChars[self.rank] + Card.suitChars[self.suit]


################################################################################
# simulation

def simulate(numGames):
    rand = random.Random()
    rand.seed(2)
    gameScores = []

    for gameIdx in range(numGames):
        print("game={:03}".format(gameIdx))

        claimedHandTypeToScore = {}

        for roundIdx in range(8):
            print("    round={}".format(roundIdx))

            rolls = [randomCardStrs(5, rand)]

            for rollIdx in range(3):
                print("        dice={}".format(','.join(rolls[-1])))

                choice = poker_dice(rolls, claimedHandTypeToScore)

                if isinstance(choice, str):
                    print("        claim={}".format(choice))
                    if choice in g_handTypeToScore:
                        claimedHandTypeToScore[choice] \
                            = g_handTypeToScore[choice]
                    break
                else:
                    print("        keep={}".format(','.join(choice)))
                    newRoll = choice + randomCardStrs(5 - len(choice), rand)
                    rolls.append(newRoll)

            roundScore = sum(claimedHandTypeToScore.values())
            print("        score={:03}".format(roundScore))

        gameScore = sum(claimedHandTypeToScore.values())
        print("    finalScore={:03}".format(gameScore))
        gameScores.append(gameScore)

    print("avgGameScore={}".format(sum(gameScores) / len(gameScores)))


def getAvgScoreOfChoice(rolls, claimedHandTypeToScore, choice):
    if len(rolls) == 3 or isinstance(choice, str):
        return scoreWithChoice(claimedHandTypeToScore, choice)

    numTrials = 50 if len(choice) < 5 else 1
    scoreSum = 0

    for trialIdx in range(numTrials):
        newRolls = rolls + [choice + randomCardStrs(5 - len(choice))]

        newChoice = poker_dice(newRolls, claimedHandTypeToScore)

        avgScoreOfNewChoice = getAvgScoreOfChoice(
            newRolls, claimedHandTypeToScore, newChoice)

        scoreSum += avgScoreOfNewChoice

    return scoreSum / numTrials


def scoreWithChoice(claimedHandTypeToScore, choice):
    choiceScoreDelta = 0

    if isinstance(choice, str):
        if choice in g_handTypeToScore and choice not in claimedHandTypeToScore:
            choiceScoreDelta = g_handTypeToScore[choice]

    return choiceScoreDelta + sum(claimedHandTypeToScore.values())


def randomCardStrs(numCards, rand=random):
    return [
        rand.choice(Card.rankChars) + rand.choice(Card.suitChars)
        for cardIdx in range(numCards)
    ]


################################################################################
# decider

def poker_dice_old(rolls, claimedHandTypeToScore):
    numRollsLeft = 3 - len(rolls)
    cards = [Card.fromStr(cardStr) for cardStr in rolls[-1]]

    handInfos = getBestHandInfos(cards)

    if numRollsLeft == 0:
        for handType, hand in handInfos:
            if handType not in claimedHandTypeToScore:
                return handType

        # maybe will get lucky and reclaim hand but with aces
        if handInfos:
            return handInfos[0][0]

        return "no hand to claim"

    else:
        if handInfos:
            return [str(card) for card in handInfos[0][1]]

        # default is to keep aces for slight score bonus
        return [str(card) for card in cards if card.rank == Card.aceRank]


def poker_dice(rolls, claimedHandTypeToScore):
    numRollsLeft = 3 - len(rolls)
    cards = [Card.fromStr(cardStr) for cardStr in rolls[-1]]


    if numRollsLeft == 0:
        handInfos = getBestHandInfos(cards)

        for handType, hand in handInfos:
            if handType not in claimedHandTypeToScore:
                return handType

        # maybe will get lucky and reclaim hand but with aces
        if handInfos:
            return handInfos[0][0]

        return g_highCards

    else:
        # TODO: instead of trying all subsets of cards to keep, try:
        # cards of best hand
        # the triple if we have full house
        # cards of most common suit (for flush attempt)
        # at most one ace
        # all aces
        # and make sure each subset of cards is unique before branching
        bestScore = -1
        bestKeptCards = []
        keptCardsHist = {}

        for numKeepCards in range(5):
            for keptCards in itertools.combinations(rolls[-1], numKeepCards):
                if keptCards in keptCardsHist:
                    continue

                keptCardList = list(keptCards)

                avgScore = getAvgScoreOfChoice(
                    rolls, claimedHandTypeToScore, keptCardList)

                keptCardsHist[keptCards] = avgScore

                if avgScore > bestScore:
                    bestScore = avgScore
                    bestKeptCards = keptCardList

        return bestKeptCards


def getBestHandInfos(cards):
    if isinstance(cards[0], str):
        cards = [Card.fromStr(cardStr) for cardStr in cards]

    rankToCards = collections.defaultdict(list)

    for card in cards:
        rankToCards[card.rank].append(card)

    countToCards = collections.defaultdict(list)

    for rank, cardsOfRank in rankToCards.items():
        countToCards[len(cardsOfRank)].extend(cardsOfRank)

    handInfos = getSimpleRankMultipleHands(countToCards)

    # full house
    if 2 in countToCards and 3 in countToCards:
        handInfos.append((g_fullHouse, cards))

    # two pair
    if len(countToCards[2]) == 4:
        handInfos.append((g_twoPair, countToCards[2][:4]))

    # flush
    if len(set(card.suit for card in cards)) == 1:
        handInfos.append((g_flush, cards))

    # straight
    if len(countToCards[1]) == 5:
        if not rankToCards[Card.ranks[0]] or not rankToCards[Card.ranks[-1]]:
            handInfos.append((g_straight, cards))

    handInfos = list(reversed(sorted(
        handInfos,
        key = lambda info: g_handTypeToScore[info[0]]
    )))

    return handInfos


def getSimpleRankMultipleHands(countToCards):
    handInfos = []

    for count in range(5, 1, -1):
        if count in countToCards:
            cards = countToCards[count]
            if count >= 5:
                handInfos.append((g_fiveOfAKind, cards[:5]))
            if count >= 4:
                handInfos.append((g_fourOfAKind, cards[:4]))
            if count >= 3:
                handInfos.append((g_threeOfAKind, cards[:3]))
            if count >= 2:
                handInfos.append((g_onePair, cards[:2]))

    return handInfos


if __name__ == '__main__':
    #handInfos1 = getBestHandInfos(["9S","QH","JS","JS","QH"])
    #handInfos2 = getBestHandInfos(["9S","QS","JS","TS","KS"])
    #handInfos3 = getBestHandInfos(["9S","JS","9S","JH","JH"])
    simulate(1)
    print()

