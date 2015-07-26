'''
author: Jacob Egner
date: 2015-07-26
island: electronic station

puzzle prompt:
http://www.checkio.org/mission/how-much-gold/

puzzle prompt source repo:
https://github.com/Bryukh-Checkio-Tasks/checkio-task-how-much-gold

my checkio solution repo:
https://github.com/jmegner/CheckioPuzzles

my solution relies on the fact that since each alloy has two metals, overall
metals are double-counted when looking at the list of alloy fractions

'''


from fractions import Fraction


METALS = ('gold', 'tin', 'iron', 'copper')


def checkio(alloyToFraction):
    nonGoldFractions = []

    for alloy in alloyToFraction:
        if 'gold' in alloy:
            nonGoldFractions.append((1 - alloyToFraction[alloy]) / 2)
        else:
            nonGoldFractions.append(alloyToFraction[alloy] / 2)

    return 1 - sum(nonGoldFractions)


if __name__ == '__main__':
    assert checkio({
        'gold-tin': Fraction(1, 2),
        'gold-iron': Fraction(1, 3),
        'gold-copper': Fraction(1, 4),
        }) == Fraction(1, 24), "1/24 of gold"

    assert checkio({
        'tin-iron': Fraction(1, 2),
        'iron-copper': Fraction(1, 2),
        'copper-tin': Fraction(1, 2),
        }) == Fraction(1, 4), "quarter"

