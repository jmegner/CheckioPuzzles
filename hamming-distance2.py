def checkio(n, m):
    # xor to get bit differences, then sum them with help of map
    # string slice starts at 2 to get rid of leading "0b" from bin()
    return sum(map(int, bin(n ^ m)[2:]))


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert checkio(117, 17) == 3, "First example"
    assert checkio(1, 2) == 2, "Second example"
    assert checkio(16, 15) == 5, "Third example"
