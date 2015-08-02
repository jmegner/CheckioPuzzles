'''
author: Jacob Egner
date: 2015-08-02
island: electronic station

puzzle URLs:
http://www.checkio.org/mission/texas-referee/
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-texas-referee

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles
'''


import collections
import functools


class Card(collections.namedtuple("Card", ["rank", "suit"])):

    rankChars = "23456789TJQKA"
    suitChars = "scdh"
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


def texas_referee(cardsStr):
    cards = list(reversed(sorted([
        Card.fromStr(cardStr) for cardStr in cardsStr.split(',')])))

    handGetters = [
        getStraightFlush,
        getFourOfAKind,
        getFullHouse,
        getFlush,
        getStraight,
        getThreeOfAKind,
        getTwoPair,
        getOnePair,
        getHighCards,
    ]

    for handGetter in handGetters:
        partialHand = handGetter(cards)

        if partialHand:
            fullHand = (partialHand + getRemainingCards(cards, partialHand))[:5]
            handStr = ",".join(map(str, reversed(sorted(fullHand))))
            return handStr

    raise RuntimeError("should never get here")


def getRemainingCards(allCards, usedCards):
    return list(reversed(sorted(set(allCards) - set(usedCards))))


def getStraightFlush(sortedCards):
    for topCard in sortedCards:
        neededCards = [Card(topCard.rank - rankOffset, topCard.suit)
            for rankOffset in range(5)]

        if all(neededCard in sortedCards for neededCard in neededCards):
            return neededCards

    return []


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


getFourOfAKind  = functools.partial(getRankMultiples, cardCounts=[4])
getFullHouse    = functools.partial(getRankMultiples, cardCounts=[3, 2])
getThreeOfAKind = functools.partial(getRankMultiples, cardCounts=[3])
getTwoPair      = functools.partial(getRankMultiples, cardCounts=[2, 2])
getOnePair      = functools.partial(getRankMultiples, cardCounts=[2])
getHighCards    = functools.partial(getRankMultiples, cardCounts=[1]*5)


if __name__ == '__main__':
    assert texas_referee("Kh,Qh,Ah,9s,2c,Th,Jh") == "Ah,Kh,Qh,Jh,Th", "High Straight Flush"
    assert texas_referee("Qd,Ad,9d,8d,Td,Jd,7d") == "Qd,Jd,Td,9d,8d", "Straight Flush"
    assert texas_referee("5c,7h,7d,9s,9c,8h,6d") == "9c,8h,7h,6d,5c", "Straight"
    assert texas_referee("Ts,2h,2d,3s,Td,3c,Th") == "Th,Td,Ts,3c,3s", "Full House"
    assert texas_referee("Jh,Js,9h,Jd,Th,8h,Td") == "Jh,Jd,Js,Th,Td", "Full House vs Flush"
    assert texas_referee("Js,Td,8d,9s,7d,2d,4d") == "Td,8d,7d,4d,2d", "Flush"
    assert texas_referee("Ts,2h,Tc,3s,Td,3c,Th") == "Th,Td,Tc,Ts,3c", "Four of Kind"
    assert texas_referee("Ks,9h,Th,Jh,Kd,Kh,8s") == "Kh,Kd,Ks,Jh,Th", "Three of Kind"
    assert texas_referee("2c,3s,4s,5s,7s,2d,7h") == "7h,7s,5s,2d,2c", "Two Pairs"
    assert texas_referee("2s,3s,4s,5s,2d,7h,8h") == "8h,7h,5s,2d,2s", "One Pair"
    assert texas_referee("3h,4h,Th,6s,Ad,Jc,2h") == "Ad,Jc,Th,6s,4h", "High Cards"

