'''
author: Jacob Egner
date: 2015-07-27
island: elementary

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


def checkio(text1, text2):
    commonWords = set(
        word1
        for word1 in text1.split(',')
        for word2 in text2.split(',')
        if word1 == word2
    )

    return ','.join(sorted(commonWords))


if __name__ == '__main__':
    assert checkio("hello,world", "hello,earth") == "hello", "Hello"
    assert checkio("one,two,three", "four,five,six") == "", "Too different"
    assert checkio("one,two,three", "four,five,one,two,six,three") == "one,three,two", "1 2 3"


