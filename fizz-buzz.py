'''
author: Jacob Egner
date: 2015-07-27
island: elementary

puzzle prompt:
http://www.checkio.org/mission/fizz-buzz/

puzzle prompt source repo:
https://github.com/Bryukh-Checkio-Tasks/checkio-task-fizz-buzz

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


def checkio(number):
    if number % 3 == 0 and number % 5 == 0:
        return "Fizz Buzz"

    if number % 3 == 0:
        return "Fizz"

    if number % 5 == 0:
        return "Buzz"

    return str(number)


if __name__ == '__main__':
    assert checkio(15) == "Fizz Buzz", "15 is divisible by 3 and 5"
    assert checkio(6) == "Fizz", "6 is divisible by 3"
    assert checkio(5) == "Buzz", "5 is divisible by 5"
    assert checkio(7) == "7", "7 is not divisible by 3 or 5"


