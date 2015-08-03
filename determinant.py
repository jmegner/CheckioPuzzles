'''
author: Jacob Egner
date: 2015-08-02
island: ice base

puzzle URLs:
http://www.checkio.org/mission/determinant/
https://github.com/Bryukh-Checkio-Tasks/checkio-task-determinant

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

Solution Overview:
I use the Laplace expansion to compute determinants.
https://en.wikipedia.org/wiki/Laplace_expansion
'''


def checkio(data):
    return determinant(data)


def determinant(data):
    if len(data) == 1:
        return data[0][0]

    terms = [ data[0][c] * cofactor(data, 0, c) for c in range(len(data[0]))]
    return sum(terms)


def cofactor(data, r, c):
    codata = []

    sideLen = len(data)
    codata = [
        [data[r2][c2] for c2 in range(sideLen) if c2 != c]
        for r2 in range(sideLen) if r2 != r
    ]

    return determinant(codata) * (-1) ** (r + c)


if __name__ == '__main__':
    assert checkio([
        [4, 3],
        [6, 3],
        ]) == -6, 'First example'

    assert checkio([
        [1, 3, 2],
        [1, 1, 4],
        [2, 2, 1],
        ]) == 14, 'Second example'

    assert checkio([
        [4, 8, 7, 6],
        [4, 8, 3, 9],
        [0, 5, 3, 4],
        [4, 5, 3, 5],
        ]) == -20, 'Extra 19, I think'

