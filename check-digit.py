'''
author: Jacob Egner
date: 2015-07-31
island: ice base

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

I did not enjoy this puzzle.  The prompt made it very difficult to understand
what was wanted, and the puzzle itself feels arbitrary and uninteresting.

'''


def checkio(rawStr):
    charSum = 0
    cleanChars = [char.upper() for char in reversed(rawStr) if char.isalnum()]

    for charIdx, char in enumerate(cleanChars):
        charVal = ord(char) - ord('0')

        if charIdx % 2 == 0:
            charVal = sum(divmod(charVal * 2, 10))

        charSum += charVal

    return [str(-charSum % 10), charSum]


if __name__ == '__main__':
    assert (checkio("799 273 9871") == ["3", 67]), "First Test"
    assert (checkio("139-MT") == ["8", 52]), "Second Test"
    assert (checkio("123") == ["0", 10]), "Test for zero"
    assert (checkio("999_999") == ["6", 54]), "Third Test"
    assert (checkio("+61 820 9231 55") == ["3", 37]), "Fourth Test"
    assert (checkio("VQ/WEWF/NY/8U") == ["9", 201]), "Fifth Test"

