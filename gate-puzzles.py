'''
author: Jacob Egner
date: 2015-07-26
island: electronic station

puzzle prompt:
http://www.checkio.org/mission/gate-puzzles

puzzle prompt source repo:
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-gate-puzzle

my checkio solution repo:
https://github.com/jmegner/CheckioPuzzles

note: puzzle also titled "Moria doors"

'''


import string


def find_word(message):
    words = [token.strip(string.punctuation).lower() for token
        in reversed(message.split(' '))]

    scores = [sum([likeness(word1, word2) for word2 in words]) for word1 in words]
    bestScore = max(scores)

    return words[scores.index(bestScore)]


def likeness(word1, word2):
    score = 0

    if word1[0] == word2[0]:
        score += 1

    if word1[-1] == word2[-1]:
        score += 1

    score += 3 * min(len(word1) / len(word2), len(word2) / len(word1))
    score += 5 * len(set(word1) & set(word2)) / len(set(word1) | set(word2))

    return score


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert find_word("Speak friend and enter.") == "friend", "Friend"
    assert find_word("Beard and Bread") == "bread", "Bread is Beard"
    assert find_word("The Doors of Durin, Lord of Moria. Speak friend and enter. "
                     "I Narvi made them. Celebrimbor of Hollin drew these signs") == "durin", "Durin"
    assert find_word("Aoccdrnig to a rscheearch at Cmabrigde Uinervtisy."
                     " According to a researcher at Cambridge University.") == "according", "Research"
    assert find_word("One, two, two, three, three, three.") == "three", "Repeating"
