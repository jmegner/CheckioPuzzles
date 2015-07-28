'''
author: Jacob Egner
date: 2015-07-27
island: elementary

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


def checkio(words):
    for word1 in words:
        for word2 in words:
            if(word1 != word2
                and 0 <= word1.rfind(word2) == len(word1) - len(word2)
            ):
                return True

    return False

    ''' following works but it less clear and less debugger-friendly:
    return any(
        word1.rfind(word2) == len(word1) - len(word2)
        for word1 in words for word2 in words
    )
    '''

#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio({"hello", "lo", "he"}) == True, "helLO"
    assert checkio({"hello", "la", "hellow", "cow"}) == False, "hellow la cow"
    assert checkio({"walk", "duckwalk"}) == True, "duck to walk"
    assert checkio({"one"}) == False, "Only One"
    assert checkio({"helicopter", "li", "he"}) == False, "Only end"
