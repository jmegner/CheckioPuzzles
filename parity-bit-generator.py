'''
author: Jacob Egner
date: 2015-08-25
island: no island assigned yet

puzzle URLs:
http://www.checkio.org/mission/parity-bit-generator/
https://github.com/tivaliy/checkio-task-parity-bit-generator

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles
'''


def checkio(paritiedData):
    correctChars = []

    for datum in paritiedData:
        if bin(datum).count('1') % 2 == 0:
            correctChars.append(chr(datum >> 1))

    message = ''.join(correctChars)
    return message

    # or, to put it as a less-readable one-liner...
    # return ''.join(chr(x>>1) for x in paritiedData if 1-bin(x).count('1')%2)


if __name__ == '__main__':
    assert checkio([
        135, 134, 124, 233,
        209, 81, 42, 202,
        198, 194, 229, 215,
        230, 146, 28, 210,
        145, 137, 222, 158,
        49, 81, 214, 157,
    ]) == "Checkio"

    assert checkio([
        144, 100, 200, 202,
        216, 152, 164, 88,
        216, 222, 65, 218,
        175, 217, 248, 222,
        171, 228, 216, 205,
        254, 201, 193, 220,
    ]) == "Hello World"

