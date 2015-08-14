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


import datetime
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


class Card(str):

    allCards = ("9S", "TH", "JS", "QH", "KH", "AS")
    rankChars = "9TJQKA"
    suitChars = "SH"
    ranks = tuple(range(len(rankChars)))
    suits = tuple(range(len(suitChars)))
    lowRank = 0
    highRank = 5

    def rankChar(self): return self[0]
    def suitChar(self): return self[1]
    def rank(self): return self.rankChars.index(self.rankChar())
    def suit(self): return self.suitChars.index(self.suitChar())


################################################################################
# simulation

def simulate(numGames):
    rand = random.Random()
    #rand.seed(2)
    gameScores = []

    for gameIdx in range(numGames):
        print("game={:03}".format(gameIdx))

        claimedHandTypeToScore = {}

        for roundIdx in range(8):
            print("    round={}".format(roundIdx))
            print("        prevClaims: {}".format(
                ", ".join(claimedHandTypeToScore.keys())))

            rolls = [randomCards(5, rand)]

            for rollIdx in range(3):
                print("        dice={}".format(','.join(rolls[-1])))

                choice = poker_dice(rolls, claimedHandTypeToScore.copy())

                if isinstance(choice, str):
                    print("        claim={}".format(choice))
                    if choice in g_handTypeToScore:
                        claimedHandTypeToScore[choice] \
                            = g_handTypeToScore[choice]
                    break
                else:
                    print("        keep={}".format(','.join(choice)))
                    newRoll = choice + randomCards(5 - len(choice), rand)
                    rolls.append(newRoll)

            roundScore = sum(claimedHandTypeToScore.values())
            print("        score={:03}".format(roundScore))

        gameScore = sum(claimedHandTypeToScore.values())
        print("    finalScore={:03}".format(gameScore))
        gameScores.append(gameScore)

    avgGameScore = sum(gameScores) / len(gameScores)
    pentaGameScore = 5 * avgGameScore
    print("gameScores: max={}, avg={}, avgPenta={}".format(
        max(gameScores), avgGameScore, pentaGameScore))


################################################################################
# decider

def poker_dice(rolls, claimedHandTypeToScore, focusOnFiveOfAKind=False):
    '''
    focusOnFiveOfAKind being True tries to maximize chances of getting a high
    score; focusOnFiveOfAKind being False tries to maximize your average score
    '''

    numRollsLeft = 3 - len(rolls)
    cards = [Card(card) for card in rolls[-1]]
    cards = sorted(cards, key = lambda card: -card.rank())

    handInfos = getBestHandInfos(cards)

    if numRollsLeft == 0:
        for handType, hand in handInfos:
            if handType not in claimedHandTypeToScore:
                return handType

        # maybe will get lucky and reclaim hand but with aces
        if handInfos:
            return handInfos[0][0]

        return g_highCards

    else:
        if focusOnFiveOfAKind and g_fiveOfAKind not in claimedHandTypeToScore:
            bestHandTypesForFutureFiveOfAKind = [
                g_fiveOfAKind, g_fourOfAKind, g_threeOfAKind, g_onePair,
            ]

            for handType, hand in handInfos:
                if handType in bestHandTypesForFutureFiveOfAKind:
                    return hand

            return getAces(cards)

        trialHands = []

        if handInfos:
            # cards of best hand
            trialHands.append(handInfos[0][1])

            # triple if we have a full house
            for handType, hand in handInfos:
                if handType == g_fullHouse:
                    trialHands.append(hand[3:])
                    break

            # one pair if we have two pair
            for handType, hand in handInfos:
                if handType == g_twoPair:
                    trialHands.append(hand[:2])
                    break

        # flush attempt
        if g_flush not in claimedHandTypeToScore:
            suitCharToCards = collections.defaultdict(list)

            for card in cards:
                suitCharToCards[card.suitChar()].append(card)

            flushAttempt = max(suitCharToCards.values(), key=len)
            trialHands.append(flushAttempt)

        # straight attempt
        if g_straight not in claimedHandTypeToScore:
            straightAttempt = []

            for card in cards:
                if card not in straightAttempt:
                    straightAttempt.append(card)

            # straight impossible if have both 9 and ace
            if(Card.allCards[0] in straightAttempt
                and Card.allCards[-1] in straightAttempt
            ):
                straightAttempt.remove(Card.allCards[0])

            trialHands.append(straightAttempt)

        atMostOneAce = getAces(cards)
        trialHands.append(atMostOneAce)

        bestScore = -1
        bestTrialHand = []

        for trialHand in trialHands:

            expectedScore = getAvgScoreOfChoice(
                rolls, claimedHandTypeToScore, trialHand)

            if expectedScore > bestScore:
                bestScore = expectedScore
                bestTrialHand = trialHand

        if len(bestTrialHand) == 5:
            for handType, hand in handInfos:
                if hand == bestTrialHand:
                    return handType

        return bestTrialHand


def getAces(cards):
    return [card for card in cards if card.rank() == Card.highRank]


def getAvgScoreOfChoice(rolls, claimedHandTypeToScore, choice):
    numRollsLeft = 3 - len(rolls)

    if numRollsLeft == 0 or isinstance(choice, str):
        return scoreWithChoice(claimedHandTypeToScore, choice)

    multis = getMultiplicities(getCountToCards(
        getRankCharToCards(choice)))

    expectedScore = scoreWithChoice(claimedHandTypeToScore, "")

    if g_fiveOfAKind not in claimedHandTypeToScore:
        prob = alterProb(getProbFiveOfAKind(multis), numRollsLeft)
        expectedScore += prob * g_handTypeToScore[g_fiveOfAKind]

    if g_fourOfAKind not in claimedHandTypeToScore:
        prob = alterProb(getProbFourOfAKind(multis), numRollsLeft)
        expectedScore += prob * g_handTypeToScore[g_fourOfAKind]

    if g_threeOfAKind not in claimedHandTypeToScore:
        prob = alterProb(getProbThreeOfAKind(multis), numRollsLeft)
        expectedScore += prob * g_handTypeToScore[g_threeOfAKind]

    if g_onePair not in claimedHandTypeToScore:
        prob = alterProb(getProbOnePair(multis), numRollsLeft)
        expectedScore += prob * g_handTypeToScore[g_onePair]

    if g_fullHouse not in claimedHandTypeToScore:
        prob = alterProb(getProbFullHouse(multis), numRollsLeft)
        expectedScore += prob * g_handTypeToScore[g_fullHouse]

    if g_twoPair not in claimedHandTypeToScore:
        prob = alterProb(getProbTwoPair(multis), numRollsLeft)
        expectedScore += prob * g_handTypeToScore[g_twoPair]

    if g_flush not in claimedHandTypeToScore:
        suitCounts = [0, 0]
        for card in choice:
            suitCounts[card.suit()] += 1

        prob = alterProb(getProbFlush(max(suitCounts)), numRollsLeft)
        expectedScore += prob * g_handTypeToScore[g_flush]

    if g_straight not in claimedHandTypeToScore:
        ranks = [card.rank() for card in choice]
        prob = alterProb(
            getProbStraight(ranks, multis),
            numRollsLeft)
        expectedScore += prob * g_handTypeToScore[g_straight]

    return expectedScore


def alterProb(prob, numAttempts):
    if numAttempts <= 1:
        return prob

    return 1 - (1 - prob) ** numAttempts


def scoreWithChoice(claimedHandTypeToScore, choice):
    choiceScoreDelta = 0

    if isinstance(choice, str):
        if choice in g_handTypeToScore and choice not in claimedHandTypeToScore:
            choiceScoreDelta = g_handTypeToScore[choice]

    return choiceScoreDelta + sum(claimedHandTypeToScore.values())


def randomCards(numCards, rand=random):
    return [rand.choice(Card.allCards) for cardIdx in range(numCards)]


def getBestHandInfos(cards):
    rankCharToCards = getRankCharToCards(cards)
    countToCards = getCountToCards(rankCharToCards)
    handInfos = getSimpleRankMultipleHands(countToCards)

    # full house
    if 2 in countToCards and 3 in countToCards:
        handInfos.append((g_fullHouse, cards))

    # two pair
    if len(countToCards[2]) == 4:
        handInfos.append((g_twoPair, countToCards[2][:4]))

    # flush
    if len(set(card.suitChar() for card in cards)) == 1:
        handInfos.append((g_flush, cards))

    # straight
    if len(countToCards[1]) == 5:
        if(not rankCharToCards[Card.ranks[0]]
            or not rankCharToCards[Card.ranks[-1]]
        ):
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


def getRankCharToCards(cards):
    rankCharToCards = collections.defaultdict(list)

    for card in cards:
        rankCharToCards[card.rank()].append(card)

    return rankCharToCards


def getCountToCards(rankCharToCards):
    countToCards = collections.defaultdict(list)

    for rank, cardsOfRank in rankCharToCards.items():
        count = len(cardsOfRank)
        countToCards[count] = sorted(
            countToCards[count] + cardsOfRank,
            key = lambda card: -card.rank()
        )

    return countToCards


def getMultiplicities(countToCards):
    if not countToCards:
        return [0]
    elif 2 in countToCards and len(countToCards[2]) == 4:
        return [2, 2]
    elif 2 in countToCards and 3 in countToCards:
        return [3, 2]
    else:
        return [max(countToCards.keys())]


def getProbFiveOfAKind(multis):
    if len(multis) > 1:
        return 0
    return (1 / 6) ** (5 - multis[0])


def getProbFourOfAKind(multis):
    if len(multis) > 1:
        return 0
    if multis[0] >= 4:
        return 1
    if multis[0] == 3:
        return 11 / 36
    if multis[0] == 2:
        return 16 / 216
    return 21 / 1296


def getProbThreeOfAKind(multis):
    if multis == [3, 2]:
        return 1
    if multis == [2, 2]:
        return 1 / 6
    if multis[0] >= 3:
        return 1
    if multis[0] == 2:
        return 191 / 216
    return 171 / 1296


def getProbOnePair(multis):
    if multis[0] >= 2:
        return 1
    return 671 / 1296


def getProbTwoPair(multis):
    if multis == [3, 2] or multis == [2, 2]:
        return 1
    if multis[0] >= 4:
        return 0
    if multis[0] == 3:
        return 1 / 6
    if multis[0] == 2:
        return 16 / 36

    return 0.2702


def getProbFullHouse(multis):
    if multis == [3, 2]:
        return 1
    if multis == [2, 2]:
        return 1 / 3
    if multis[0] >= 4:
        return 0
    if multis[0] == 3:
        return 1 / 6
    if multis[0] == 2:
        return 6 / 216

    return 30 / 1296


def getProbFlush(multi):
    return 0.5 ** (5 - multi)


def getProbStraight(ranks, multis):
    if multis[0] > 1:
        return 0

    if not ranks:
        return  0.0309

    ranks = sorted(ranks)

    if ranks[0] == Card.lowRank and ranks[-1] == Card.highRank:
        return 0

    prob = (1/6) ** (5 - len(ranks))

    if ranks[0] != Card.lowRank and ranks[-1] != Card.highRank:
        prob *= 2

    return prob


if __name__ == '__main__':
    simulate(5)
    print(str(datetime.datetime.now()))

