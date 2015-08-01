'''
author: Jacob Egner
date: 2015-08-01
island: electronic station

puzzle URLs:
http://www.checkio.org/mission/vigenere-cipher/
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-vigenere-cipher

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles
'''


g_wrapModulus = 26
g_wrapStart = ord('A')


def decode_vigenere(oldPlain, oldCipher, newCipher):
    newPlainChars = []
    decryptOffsets = getDecryptKey(oldPlain, oldCipher)

    for charIdx, newCipherChar in enumerate(newCipher):
        newPlainChars.append(getOffsetChar(
            newCipherChar,
            decryptOffsets[charIdx % len(decryptOffsets)]
        ))

    return ''.join(newPlainChars)


def getOffsetChar(origChar, offset):
    unwrappedVal = ord(origChar) - g_wrapStart + offset
    wrappedVal = unwrappedVal % g_wrapModulus + g_wrapStart
    wrappedChar = chr(wrappedVal)
    return wrappedChar


def getDecryptKey(plain, cipher):
    textLen = len(plain)
    offsets = []

    for plainChar, cipherChar in zip(plain, cipher):
        offsets.append((ord(plainChar) - ord(cipherChar)) % g_wrapModulus)

    workingKeyLen = textLen

    for keyLen in range(1, textLen // 2 + 1):
        key = offsets[:keyLen]
        foundRepeatedKey = True

        for keyStart in range(keyLen, textLen, keyLen):
            compareChunk = offsets[keyStart : keyStart + keyLen]

            if key[:len(compareChunk)] != compareChunk:
                foundRepeatedKey = False
                break

        if foundRepeatedKey:
            return key

    return offsets


if __name__ == '__main__':
    assert decode_vigenere(
        'DONTWORRYBEHAPPY',
        'FVRVGWFTFFGRIDRF',
        'DLLCZXMFVRVGWFTF') == "BEHAPPYDONTWORRY", "key: CHECKIO"

    assert decode_vigenere('HELLO', 'OIWWC', 'ICP') == "BYE", "key: HELLO"

    assert decode_vigenere(
        'LOREMIPSUM',
        'OCCSDQJEXA',
        'OCCSDQJEXA') == "LOREMIPSUM", "key: DOLORIUM"

    plain1 =  'ANDNOWFORSOMETHINGCOMPLETELYDIFFERENT'
    cipher1 = 'PLWUCJUMKZCZTRAPBTRMFWZRICEFRVUDXYSAI'
    query1 = ('XKTSIZQCKQOPZYGKWZDIBZZRTNTSZAXEAAOASGPVFXPJEKOLX'
        'ANARBLLMYSRHGLRWCPLWQIZEGEPYRIMIYSFHUBSRSAMPLFFXN'
        'NACALMFLBFRJHAVVCETURUPLZHFBJLWPBOPPL')
    answer1 = ('IMALUMBERJACKANDIMOKISLEEPALLNIGHTANDIWORKALLDAYI'
        'CUTDOWNTREESISKIPANDJUMPILIKETOPRESSWILDFLOWERSIP'
        'UTONWOMENSCLOTHINGANDHANGAROUNDINBARS')
    key1 = 'PYTHON'
    assert decode_vigenere(plain1, cipher1, query1) == answer1, 'key: ' + key1

    assert decode_vigenere(
        'AAAAAAAAA',
        'ABABABABC',
        'ABABABABC') == 'AAAAAAAAA', 'key is ABABABABC'

