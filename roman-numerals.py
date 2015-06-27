def checkio(number):
    romanParts = []
    units =  [ 'I', 'X', 'C', 'M']
    pentas = [ 'V', 'L', 'D', None]
    #                           0  1  2  3  4  5  6  7  8  9
    remainderToNumPreUnits  = [ 0, 1, 2, 3, 1, 0, 0, 0, 0, 1, ]
    remainderToNumPentas    = [ 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, ]
    remainderToNumPostUnits = [ 0, 0, 0, 0, 0, 0, 1, 2, 3, 0, ]
    remainderToNumNextUnits = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, ]

    for tenExponent, unit in enumerate(units):
        remainder = number % 10
        number //= 10

        if pentas[tenExponent] is None:
            romanParts.append(units[tenExponent] * remainder)
        else:
            penta = pentas[tenExponent]
            nextUnit = units[tenExponent + 1]

            romanParts.append(
                unit * remainderToNumPreUnits[remainder]
                + penta * remainderToNumPentas[remainder]
                + unit * remainderToNumPostUnits[remainder]
                + nextUnit * remainderToNumNextUnits[remainder])

    print(romanParts)
    return ''.join(reversed(romanParts))


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert checkio(6) == 'VI', '6'
    assert checkio(76) == 'LXXVI', '76'
    assert checkio(499) == 'CDXCIX', '499'
    assert checkio(3888) == 'MMMDCCCLXXXVIII', '3888'
