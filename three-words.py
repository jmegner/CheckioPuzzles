'''
author: Jacob Egner
date: 2015-07-27
island: elementary

puzzle prompt and puzzle prompt source repo:
http://www.checkio.org/mission/three-words/
https://github.com/Bryukh-Checkio-Tasks/checkio-task-three-words

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


def checkio(text):
    words = text.split(' ')

    for wordTriplet in zip(words, words[1:], words[2:]):
        if all(word.isalpha() for word in wordTriplet):
            return True

    return False


if __name__ == '__main__':
    assert checkio("Hello World hello") == True, "Hello"
    assert checkio("He is 123 man") == False, "123 man"
    assert checkio("1 2 3 4") == False, "Digits"
    assert checkio("bla bla bla bla") == True, "Bla Bla"
    assert checkio("Hi") == False, "Hi"


