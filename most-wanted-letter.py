'''
author: Jacob Egner
date: 2015-06-29 or somewhat before
island: home

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles
'''


import collections


def checkio(text):
    alphaText = [elem for elem in text.lower() if elem.isalpha()]
    alphaCtr = collections.Counter(alphaText)

    orderedLettersAndCounts = sorted(
        alphaCtr.items(),
        key = lambda pair: (-pair[1], pair[0])
    )

    return orderedLettersAndCounts[0][0]


if __name__ == '__main__':
    assert checkio("Hello World!") == "l", "Hello test"
    assert checkio("How do you do?") == "o", "O is most wanted"
    assert checkio("One") == "e", "All letter only once."
    assert checkio("Oops!") == "o", "Don't forget about lower case."
    assert checkio("AAaooo!!!!") == "a", "Only letters."
    assert checkio("abe") == "a", "The First."
    print("Start the long test")
    assert checkio("a" * 9000 + "b" * 1000) == "a", "Long."
    print("The local tests are done.")


