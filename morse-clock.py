'''
author: Jacob Egner
date: 2015-07-29
island: scientific expedition

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


def checkio(timeStr):
    upperDigitBitWidths = [2, 3, 3]

    morseStr = ""

    for timePartIdx, timePartStr in enumerate(timeStr.split(":")):
        timePartStr = timePartStr.rjust(2, '0')

        morseStr += morsifyDigit(
            timePartStr[0], upperDigitBitWidths[timePartIdx])

        morseStr += " " + morsifyDigit(timePartStr[1], 4)

        if timePartIdx < 2:
            morseStr += " : "

    return morseStr


def morsifyDigit(digitStr, width):
    binaryStr = bin(int(digitStr))[2:].rjust(width, '0')
    morseStr = binaryStr.replace('0', '.').replace('1', '-')
    return morseStr


if __name__ == '__main__':
    assert checkio("10:37:49") == ".- .... : .-- .--- : -.. -..-", "First Test"
    assert checkio("21:34:56") == "-. ...- : .-- .-.. : -.- .--.", "Second Test"
    assert checkio("00:1:02") == ".. .... : ... ...- : ... ..-.", "Third Test"
    assert checkio("23:59:59") == "-. ..-- : -.- -..- : -.- -..-", "Fourth Test"


