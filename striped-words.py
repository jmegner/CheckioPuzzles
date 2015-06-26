import re


VOWELS = "AEIOUY"
CONSONANTS = "BCDFGHJKLMNPQRSTVWXZ"


def checkio(text):
    text = text.upper()
    numStripedWords = 0

    for word in re.findall(r"[a-zA-Z0-9]+", text):
        #print("word={}".format(word))
        if len(word) < 2 or not word.isalpha():
            #print("  early no")
            continue

        isStriped = True

        for letterIdx in range(1, len(word)):
            letter = word[letterIdx]
            prevLetter = word[letterIdx - 1]
            #print("  letter={}, prevLetter={}".format(letter, prevLetter))

            if not((letter in VOWELS and prevLetter in CONSONANTS)
                    or (letter in CONSONANTS and prevLetter in VOWELS)):
                #print("  disqualified")
                isStriped = False
                break

        if isStriped:
            numStripedWords = numStripedWords + 1

    return numStripedWords


#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio("My name is ...") == 3, "All words are striped"
    assert checkio("Hello world") == 0, "No one"
    assert checkio("A quantity of striped words.") == 1, "Only of"
    assert checkio("Dog,cat,mouse,bird.Human.") == 3, "Dog, cat and human"
