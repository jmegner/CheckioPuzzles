'''
author: Jacob Egner
date: 2015-07-31
island: ice base

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


def checkio(data):
    return sum(data)


if __name__ == '__main__':
    assert checkio([5, 5]) == 10, 'First'
    assert checkio([7, 1]) == 8, 'Second'
    print('All ok')

