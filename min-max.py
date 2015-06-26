def min(*args, **kwargs):
    key = kwargs.get("key", lambda x: x)
    return extreme(args, key, lambda a, b: a > b)


def max(*args, **kwargs):
    key = kwargs.get("key", lambda x: x)
    return extreme(args, key, lambda a, b: a < b)


def extreme(elems, key, keepRightArg):
    extremeElem = None

    if len(elems) == 1:
        elems = elems[0]

    for elem in elems:
        if extremeElem is None or keepRightArg(key(extremeElem), key(elem)):
            extremeElem = elem

    return extremeElem


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert max(3, 2) == 3, "Simple case max"
    assert min(3, 2) == 2, "Simple case min"
    assert max([1, 2, 0, 3, 4]) == 4, "From a list"
    assert min("hello") == "e", "From string"
    assert max(2.2, 5.6, 5.9, key=int) == 5.6, "Two maximal items"
    assert min([[1, 2], [3, 4], [9, 0]], key=lambda x: x[1]) == [9, 0], "lambda key"
