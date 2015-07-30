'''
author: Jacob Egner
date: 2015-07-29
island: electronic station

puzzle URLs:
http://www.checkio.org/mission/number-factory/
https://github.com/Bryukh-Checkio-Tasks/checkio-task-numbers-factory

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

find the prime digit factors of the number, then "up convert" the prime digit
factors into bigger digit factors if possible (8 is better than 2*2*2)

'''


import collections


def checkio(number):
    digits = getDigitFactors(number)

    if not digits:
        return 0

    return int(''.join(str(digit) for digit in digits))


def getDigitFactors(number):
    factorToPower = collections.Counter()
    primeDigits = [2, 3, 5, 7]

    for digit in primeDigits:
        while number % digit == 0:
            number //= digit
            factorToPower[digit] += 1

    if number != 1:
        return []

    # up-convert into bigger digit factors if possible;
    # 9 is better than 33, 39 is better than 333, 8 is better than 222,
    # 6 is better than 23; best to up-convert to digit factors in descending
    # order

    factorToPower[9], factorToPower[3] = divmod(factorToPower[3], 2)
    factorToPower[8], factorToPower[2] = divmod(factorToPower[2], 3)

    if factorToPower[2] and factorToPower[3]:
        factorToPower[6] += 1
        factorToPower[2] -= 1
        factorToPower[3] -= 1

    factorToPower[4], factorToPower[2] = divmod(factorToPower[2], 2)

    return sorted(factorToPower.elements())

if __name__ == '__main__':
    assert checkio(20) == 45, "1st example"
    assert checkio(21) == 37, "2nd example"
    assert checkio(17) == 0, "3rd example"
    assert checkio(33) == 0, "4th example"
    assert checkio(3125) == 55555, "5th example"
    assert checkio(9973) == 0, "6th example"
    assert checkio(1680) == 5678, "Test 11"


