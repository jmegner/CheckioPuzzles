def checkio(numWheat):
    minute = 1
    numPigeonsPresent = 1
    numPigeonsFed = 0

    while numWheat > 0:
        if numWheat >= numPigeonsPresent:
            numPigeonsFed = numPigeonsPresent
        else:
            numPigeonsFed = max(numPigeonsFed, numWheat)

        numWheat -= numPigeonsPresent
        minute += 1
        numPigeonsPresent += minute


    return numPigeonsFed

if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert checkio(1) == 1, "1st example"
    assert checkio(2) == 1, "2nd example"
    assert checkio(5) == 3, "3rd example"
    assert checkio(10) == 6, "4th example"
