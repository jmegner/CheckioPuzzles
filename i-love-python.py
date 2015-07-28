'''
author: Jacob Egner
date: 2015-07-27
island: elementary

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


def i_love_python():
    """
    often, with python's builtin functions, list comprehensions, sets, and all
    that, things that are conceptually simple in my mind are also simple in my
    code with minimal code boilerplate, unlike languages like C;

    Want to make sure that every value in an array is below some threshold? a
    simple "all(val < threshold for val in vals)" is so much better than what
    I'd have to write in C

    Also, it's always a good sign when you're writing pseudo-code, and you
    realizing you're basically writing python
    """
    return "I love Python!"


if __name__ == '__main__':
    assert i_love_python() == "I love Python!"


