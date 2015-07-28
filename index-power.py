'''
author: Jacob Egner
date: 2015-07-27
island: elementary

puzzle prompt and puzzle prompt source repo:
http://www.checkio.org/mission/index-power/
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-index-power

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


def index_power(array, idx):
    if idx >= len(array):
        return -1

    return array[idx] ** idx


if __name__ == '__main__':
    assert index_power([1, 2, 3, 4], 2) == 9, "Square"
    assert index_power([1, 3, 10, 100], 3) == 1000000, "Cube"
    assert index_power([0, 1], 0) == 1, "Zero power"
    assert index_power([1, 2], 3) == -1, "IndexError"


