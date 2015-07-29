'''
author: Jacob Egner
date: 2015-07-29
island: scientific expedition

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


def checkio(data):
    # zip(*data) returns an iterable sequence of tuples, so we have to 
    # make a list where we list-ify each tuple
    return [list(row) for row in zip(*data)]


if __name__ == '__main__':
    assert isinstance(checkio([[0]]).pop(), list) is True, "Match types"
    assert checkio(
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]) == [
            [1, 4, 7],
            [2, 5, 8],
            [3, 6, 9]], "Square matrix"

    assert checkio(
        [
            [1, 4, 3],
            [8, 2, 6],
            [7, 8, 3],
            [4, 9, 6],
            [7, 8, 1]
        ]) == [
            [1, 8, 7, 4, 7],
            [4, 2, 8, 9, 8],
            [3, 6, 3, 6, 1]], "Rectangle matrix"


