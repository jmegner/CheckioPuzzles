'''
author: Jacob Egner
date: 2015-07-14
island: mine

puzzle prompt:
http://www.checkio.org/mission/super-root

puzzle prompt source repo:
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-super-root

my checkio solution repo:
https://github.com/jmegner/CheckioPuzzles

'''


def super_root(number):
    ''' returns 'x' where x**x == number, approximately'''

    allowedError = 0.001
    guessLow = 1
    guessHigh = 10

    while True:
        guessMid = (guessLow + guessHigh) / 2.0
        superPower = guessMid ** guessMid
        residual = superPower - number

        if abs(residual) < allowedError:
            return guessMid
        elif residual < 0:
            guessLow = guessMid
        else:
            guessHigh = guessMid


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    def check_result(function, number):
        result = function(number)
        if not isinstance(result, (int, float)):
            print("The result should be a float or an integer.")
            return False
        p = result ** result
        if number - 0.001 < p < number + 0.001:
            return True
        return False
    assert check_result(super_root, 4), "Square"
    assert check_result(super_root, 9), "Cube"
    assert check_result(super_root, 81), "Eighty one"
