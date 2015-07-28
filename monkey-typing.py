'''
author: Jacob Egner
date: 2015-07-27
island: elementary

puzzle prompt and puzzle prompt source repo:
http://www.checkio.org/mission/monkey-typing/
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-monkey-typing

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


import string


def count_words(text, words):
    foundWords = set()

    for token in text.split(' '):
        token = token.strip(string.punctuation).lower()

        for word in words:
            if word in token:
                foundWords.add(word)

    return len(foundWords)


if __name__ == '__main__':
    assert count_words(
        "How aresjfhdskfhskd you?",
        {"how", "are", "you", "hello"}
        ) == 3, "Example"

    assert count_words(
        "Bananas, give me bananas!!!",
        {"banana", "bananas"}
        ) == 2, "BANANAS!"

    assert count_words(
        "Lorem ipsum dolor sit amet, consectetuer adipiscing elit.",
       {"sum", "hamlet", "infinity", "anything"}
       ) == 1, "Weird text"

