'''
author: Jacob Egner
date: 2015-07-29
island: scientific expedition

puzzle URLs:
http://www.checkio.org/mission/bag-of-santa-claus/
https://github.com/Bryukh-Checkio-Tasks/checkio-task-bag-of-santa-claus-1

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

This puzzle is simply a rephrasing of the "Secretary Problem".  Wikipedia
has a very simple solution:
https://en.wikipedia.org/wiki/Secretary_problem

'''


import math


g_bestGiftValue = 0


def choose_good_gift(currGiftValue, numGifts, currGiftIdx):
    global g_bestGiftValue

    if currGiftIdx == 1:
        g_bestGiftValue = 0

    numTrialGifts = numGifts / math.exp(1)

    if currGiftIdx < numTrialGifts:
        g_bestGiftValue = max(g_bestGiftValue, currGiftValue)
        return False

    return currGiftValue >= g_bestGiftValue


if __name__ == '__main__':
    from random import random, randint, uniform

    scale = (random() + random()) ** randint(0, 1024)

    standings = gift_count = best_gifts = 0
    bag_count = 2000
    for i in range(bag_count):
        gifts_in_bag = randint(10, 1000)
        gift_count += gifts_in_bag

        gifts = []
        selected_gift = None
        for i in range(gifts_in_bag):
            new_gift = uniform(0., scale)
            gifts.append(new_gift)
            decision = choose_good_gift(new_gift, gifts_in_bag, i + 1)
            if decision:
                selected_gift = new_gift
                gifts.extend([uniform(0., scale) for _ in range(gifts_in_bag - i - 1)])
                break
        if selected_gift is None:
            priority = len(gifts)
        else:
            priority = sum(selected_gift < x for x in gifts)
        standings += priority
        best_gifts += not priority
    print('You do won {:n} best gifts from {:n} bags with {:,} gifts!\n'
          'It seems like for bags of {:n} gifts -\n'
          'you would choose the second best gift, silver ;)'
          .format(best_gifts, bag_count, gift_count, round(gift_count / standings) + 1))


