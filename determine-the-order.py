import functools


def checkio(words):
    lessThans = {}

    # find direct less-than relations
    for word in words:
        for letterIdx, letter in enumerate(word):
            for greaterLetter in word[letterIdx + 1:]:
                lessThans.setdefault(letter, set()).add(greaterLetter)

    usualSortedAlphabet = ''.join(sorted(set(''.join(words))))

    # propagate the transitiveness of less-than
    for iteration in range(len(usualSortedAlphabet)):
        for letter in lessThans.keys():
            lessThanCopy = lessThans[letter].copy()
            for greaterLetter in lessThanCopy:
                lessThans[letter] |= lessThans.get(greaterLetter, set())

    def customLetterCmp(a, b):
        if b in lessThans.get(a, set()):
            return -1
        if a in lessThans.get(b, set()):
            return 1
        return ord(a) - ord(b)

    customSortedAlphabet = ''.join(sorted(
        usualSortedAlphabet,
        key = functools.cmp_to_key(customLetterCmp)))

    return customSortedAlphabet


#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio(["acb", "bd", "zwa"]) == "zwacbd", \
        "Just concatenate it"
    assert checkio(["klm", "kadl", "lsm"]) == "kadlsm", \
        "Paste in"
    assert checkio(["a", "b", "c"]) == "abc", \
        "Cant determine the order - use english alphabet"
    assert checkio(["aazzss"]) == "azs", \
        "Each symbol only once"
    assert checkio(["dfg", "frt", "tyg"]) == "dfrtyg", \
        "Concatenate and paste in"
