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


def poker_dice(rolls, scores):
    hand, handType = getBestHandAndType(rolls[-1])

    if handType == g_highCards:
        return []
    if handType != g_highCards:
        print("hi")
        return handType


class Card(collections.namedtuple("Card", ["rank", "suit"])):

    rankChars = "23456789TJQKA"
    suitChars = "SCDH"
    ranks = tuple(range(2, 15))
    suits = tuple(range(len(suitChars)))


    @staticmethod
    def fromStr(cardStr):
        return Card(
            Card.rankChars.index(cardStr[0]) + 2,
            Card.suitChars.index(cardStr[1])
        )


    def __str__(self):
        return Card.rankChars[self.rank - 2] + Card.suitChars[self.suit]


# TODO: return list of best hand infos: score, typeString, cardsUsed
def getBestHandAndType(cardStrs):
    cards = [Card.fromStr(cardStr) for cardStr in cardStrs]

    rankToCards = collections.defaultdict(list)

    for card in cards:
        rankToCards[card.rank].append(card)

    countToCards = collections.defaultdict(list)

    for rank, cardsOfRank in rankToCards:
        countToCards[len(cardsOfRank)].extend(cardsOfRank)

    handInfos = []
    appendChildrenOfMultiple(handInfos, countToCards)


def appendChildrenOfMultiple(handInfos, countToCards):
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


def getRemainingCards(allCards, usedCards):
    # note: duplicate cards prevent simple set operations
    remainingCtr = collections.Counter(allCards)
    remainingCtr.subtract(usedCards)
    return list(reversed(sorted(remainingCtr.elements())))


def getFlush(sortedCards):
    flushHands = []

    for suit in Card.suits:
        suitCards = [card for card in sortedCards if card.suit == suit]
        if len(suitCards) >= 5:
            flushHands.append(suitCards[:5])
        else:
            flushHands.append([])

    return max(flushHands)


def getStraight(sortedCards):
    rankToHighestCard = {card.rank : card for card in reversed(sortedCards)}

    for highRank in reversed(sorted(rankToHighestCard)):
        straightRanks = list(range(highRank, highRank - 5, -1))

        if all(rank in rankToHighestCard for rank in straightRanks):
            return [rankToHighestCard[rank] for rank in straightRanks]

    return []


def getRankMultiples(sortedCards, cardCounts):
    rankCtr = collections.Counter(sortedCards)
    cardsOfRanks = []

    for cardCount in cardCounts:
        for rank in reversed(Card.ranks):
            cardsOfRank = [card for card in sortedCards if card.rank == rank]

            if len(cardsOfRank) == cardCount:
                cardsOfRanks.extend(cardsOfRank)
                sortedCards = getRemainingCards(sortedCards, cardsOfRank)

    numTotalCardsRequested = sum(cardCounts)

    if len(cardsOfRanks) >= numTotalCardsRequested:
        return cardsOfRanks[:numTotalCardsRequested]

    return []


getFiveOfAKind  = functools.partial(getRankMultiples, cardCounts=[5])
getFourOfAKind  = functools.partial(getRankMultiples, cardCounts=[4])
getFullHouse    = functools.partial(getRankMultiples, cardCounts=[3, 2])
getThreeOfAKind = functools.partial(getRankMultiples, cardCounts=[3])
getTwoPair      = functools.partial(getRankMultiples, cardCounts=[2, 2])
getOnePair      = functools.partial(getRankMultiples, cardCounts=[2])
getHighCards    = functools.partial(getRankMultiples, cardCounts=[1]*5)


if __name__ == '__main__':
    getBestHandAndType(["9S","QH","JS","JS","QH"])

