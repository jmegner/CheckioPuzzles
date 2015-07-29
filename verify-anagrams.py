'''
author: Jacob Egner
date: 2015-07-29
island: scientific expedition

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


import collections

def verify_anagrams(text1, text2):
    counter1 = getLetterCounter(text1)
    counter2 = getLetterCounter(text2)

    return counter1 == counter2


def getLetterCounter(text):
    return collections.Counter(char.lower() for char in text if char.isalpha())


if __name__ == '__main__':
    assert isinstance(verify_anagrams("a", 'z'), bool), "Boolean!"
    assert verify_anagrams("Programming", "Gram Ring Mop") == True, "Gram of code"
    assert verify_anagrams("Hello", "Ole Oh") == False, "Hello! Ole Oh!"
    assert verify_anagrams("Kyoto", "Tokyo") == True, "The global warming crisis of 3002"


