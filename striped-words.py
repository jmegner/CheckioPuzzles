'''
author: Jacob Egner
date: 2015-07-31
island: o'reilly

puzzle URLs:
http://www.checkio.org/mission/striped-words/
https://github.com/Bryukh-Checkio-Tasks/checkio-task-striped-words

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


import re


VOWELS = "AEIOUY"
CONSONANTS = "BCDFGHJKLMNPQRSTVWXZ"


def checkio(text):
    text = text.upper()
    numStripedWords = 0

    for word in re.findall(r"[A-Z0-9]+", text):
        if len(word) < 2 or not word.isalpha():
            continue

        isStriped = True

        for letter, prevLetter in zip(word[1:], word):
            if not((letter in VOWELS and prevLetter in CONSONANTS)
                    or (letter in CONSONANTS and prevLetter in VOWELS)):
                isStriped = False
                break

        if isStriped:
            numStripedWords += 1

    return numStripedWords


if __name__ == '__main__':
    assert checkio("My name is ...") == 3, "All words are striped"
    assert checkio("Hello world") == 0, "No one"
    assert checkio("A quantity of striped words.") == 1, "Only of"
    assert checkio("Dog,cat,mouse,bird.Human.") == 3, "Dog, cat and human"


