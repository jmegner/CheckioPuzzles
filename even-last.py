'''
author: Jacob Egner
date: 2015-07-27
island: elementary

puzzle prompt and puzzle prompt source repo:
http://www.checkio.org/mission/even-last/
https://github.com/Bryukh-Checkio-Tasks/checkio-task-even-last

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


def checkio(array):
    if not array:
        return 0

    return sum(val for idx, val in enumerate(array) if idx % 2 == 0) * array[-1]


if __name__ == '__main__':
    assert checkio([0, 1, 2, 3, 4, 5]) == 30, "(0+2+4)*5=30"
    assert checkio([1, 3, 5]) == 30, "(1+5)*5=30"
    assert checkio([6]) == 36, "(6)*6=36"
    assert checkio([]) == 0, "An empty array = 0"


