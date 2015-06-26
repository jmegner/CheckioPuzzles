def rotate(goodCannons, usedPipeNumbers):
    goodRotations = []

    for rotateCount in range(len(goodCannons)):
        rotationGood = True

        for cannonIdx in usedPipeNumbers:
            if not goodCannons[cannonIdx]:
                rotationGood = False
                break

        if rotationGood:
            goodRotations.append(rotateCount)

        # rotate for next loop iteration
        goodCannons.insert(0, goodCannons.pop())

    return goodRotations


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert rotate([1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1], [0, 1]) == [1, 8], "Example"
    assert rotate([1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1], [0, 1, 2]) == [], "Mission impossible"
    assert rotate([1, 0, 0, 0, 1, 1, 0, 1], [0, 4, 5]) == [0], "Don't touch it"
    assert rotate([1, 0, 0, 0, 1, 1, 0, 1], [5, 4, 5]) == [0, 5], "Two cannonballs in the same pipe"
