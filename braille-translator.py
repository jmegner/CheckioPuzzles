'''
author: Jacob Egner
date: 2015-07-31
island: scientific expedition

puzzle URLs:
http://www.checkio.org/mission/braille-translator/
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-braille-translator

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


def convert(code):
    bin_code = bin(code)[2:].zfill(6)[::-1]
    return [[int(bin_code[j + i * 3]) for i in range(2)] for j in range(3)]


LETTERS_NUMBERS = list(map(convert, [
    1, 3, 9, 25, 17, 11, 27, 19, 10, 26,
    5, 7, 13, 29, 21, 15, 31, 23, 14, 30,
    37, 39, 62, 45, 61, 53, 47, 63, 55, 46, 26
]))

CAPITAL_FORMAT = convert(32)
NUMBER_FORMAT = convert(60)
WHITESPACE = convert(0)

PUNCTUATION = {
    ",": convert(2),
    "-": convert(18),
    "?": convert(38),
    "!": convert(22),
    ".": convert(50),
    "_": convert(36),
    " ": convert(0),
}

SYMBOLS_PER_LINE = 10
CELLS_PER_LINE = 3 * SYMBOLS_PER_LINE - 1


def braille_page(text: str):
    grid = []

    for char in text:
        if char.isalpha():
            if char.isupper():
                addSymbol(grid, CAPITAL_FORMAT)

            addSymbol(grid, LETTERS_NUMBERS[ord(char.lower()) - ord('a')])

        elif char.isnumeric():
            addSymbol(grid, NUMBER_FORMAT)
            addSymbol(grid, LETTERS_NUMBERS[(ord(char) - ord('1')) % 10])

        else:
            addSymbol(grid, PUNCTUATION[char])

    postPadBlanks(grid)

    return grid


def addSymbol(grid, symbol):
    if not grid or len(grid[-1]) % CELLS_PER_LINE == 0:
        if len(grid):
            grid.append([0] * CELLS_PER_LINE)
        grid.extend([[], [], [],])

    shouldAddColGap = len(grid[-1]) > 0

    for textRow, symbolRow in zip(grid[-3:], symbol):
        if shouldAddColGap:
            textRow.append(0)
        textRow.extend(symbolRow)


def postPadBlanks(grid):
    if len(grid) <= 3:
        return

    numCellsLacking = CELLS_PER_LINE - len(grid[-1])

    for textRow in grid[-3:]:
        textRow.extend([0] * numCellsLacking)


if __name__ == '__main__':
    def checker(func, text, answer):
        result = func(text)
        return answer == tuple(tuple(row) for row in result)

    assert checker(braille_page, "hello 1st World!", (
        (1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1),
        (1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1),
        (0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0))
    ), "Example"

    assert checker(braille_page, "42", (
        (0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0),
        (0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0),
        (1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0))), "42"

    assert checker(braille_page, "CODE", (
        (0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1),
        (0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0))
    ), "CODE"


