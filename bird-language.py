VOWELS = "aeiouy"

def translate(phrase):
    translatedPhrase = ''
    charIdx = 0

    while charIdx < len(phrase):
        char = phrase[charIdx]

        translatedPhrase += char

        if char == ' ':
            charIdx += 1
        elif char in VOWELS:
            # increment three to get past next 2 vowels
            charIdx += 3
        else:
            # increment two to get past next 1 vowels
            charIdx += 2

    return translatedPhrase

if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert translate("hieeelalaooo") == "hello", "Hi!"
    assert translate("hoooowe yyyooouuu duoooiiine") == "how you doin", "Joey?"
    assert translate("aaa bo cy da eee fe") == "a b c d e f", "Alphabet"
    assert translate("sooooso aaaaaaaaa") == "sos aaa", "Mayday, mayday"
