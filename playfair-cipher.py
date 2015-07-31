'''
author: Jacob Egner
date: 2015-07-30
island: scientific expedition

puzzle URLs:
http://www.checkio.org/mission/playfair-cipher/
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-playfair-cipher

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


def encode(plaintext, keyStr):
    return transform(plaintext, keyStr, doDecode=False)


def decode(ciphertext, keyStr):
    return transform(ciphertext, keyStr, doDecode=True)


def transform(origText, keyStr, doDecode = False):
    keyGrid = getKeyGrid(keyStr)

    midChars = prepareText(origText)
    digraphs = [
        midChars[2 * digraphIdx : 2 * (digraphIdx + 1)]
        for digraphIdx in range(0, len(midChars) // 2)
    ]

    finalChars = []
    locShift = -1 if doDecode else +1

    for digraph in digraphs:
        r1, c1 = getGridLoc(keyGrid, digraph[0])
        r2, c2 = getGridLoc(keyGrid, digraph[1])

        if r1 == r2:
            c1 = (c1 + locShift) % len(keyGrid[r1])
            c2 = (c2 + locShift) % len(keyGrid[r2])
        elif c1 == c2:
            r1 = (r1 + locShift) % len(keyGrid)
            r2 = (r2 + locShift) % len(keyGrid)
        else:
            c1, c2 = c2, c1

        finalChars.append(keyGrid[r1][c1])
        finalChars.append(keyGrid[r2][c2])

    return ''.join(finalChars)



def getKeyGrid(keyStr):
    keyStr = keyStr.lower() + "abcdefghijklmnopqrstuvwxyz0123456789"

    keyList = []

    for keyChar in keyStr:
        if keyChar not in keyList:
            keyList.append(keyChar)

    sideLen = 6
    keyGrid = [
        keyList[rowStart : rowStart + sideLen] for rowStart
        in range(0, sideLen**2, sideLen)
    ]
    return keyGrid


def prepareText(plaintext):
    plainChars = [char.lower() for char in plaintext if char.isalnum()]
    midChars = []

    for char, prevChar in zip(plainChars, [' '] + plainChars):
        if char == prevChar and len(midChars) % 2 == 1:
            if prevChar == 'x':
                midChars.append('z')
            else:
                midChars.append('x')

        midChars.append(char)

    if len(midChars) % 2 == 1:
        if midChars[-1] == 'z':
            midChars.append('x')
        else:
            midChars.append('z')

    return midChars


def getGridLoc(grid, searchChar):
    for r, row in enumerate(grid):
        if searchChar in row:
            return (r, row.index(searchChar))

    raise ValueError("could not find searchChar")


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert encode("Fizz Buzz is x89 XX.", "checkio101") == 'do2y7mt22kry94y2y2', "Encode fizz buzz"
    assert decode("do2y7mt22kry94y2y2", "checkio101") == 'fizxzbuzzisx89xzxz', "Decode fizz buzz"
    assert encode("How are you?", "hello") == 'ea2imb1ht0', "Encode How are you"
    assert decode("ea2imb1ht0", "hello") == 'howareyouz', "Decode How are you"
    assert encode("My name is Alex!!!", "alexander") == 'i1dlkxjqlexn', "Encode Alex"
    assert decode("i1dlkxjqlexn", "alexander") == 'mynameisalex', "Decode Alex"
    assert encode("Who are you?", "human") == 'rnvftc1jd5', "Encode WHo"
    assert decode("rnvftc1jd5", "human") == 'whoareyouz', "Decode Who"
    assert encode("ATTACK AT DAWN", "general") == 'ewwektewhnua', "Encode attack"
    assert decode("ewwektewhnua", "general") == 'attackatdawn', "Decode attack"


