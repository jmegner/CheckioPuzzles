'''
author: Jacob Egner
date: 2015-07-31
island: electronic station

puzzle URLs:
http://www.checkio.org/mission/cowsay/
https://github.com/Cjkjvfnby/checkio-task-what-does-the-cow-say
https://github.com/omfgnuts/checkio-task-what-does-the-cow-say

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles
'''


COW = r'''
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
'''


def cowsay(text):
    textLines = getTextLines(text)
    bubbleLines = getBubbleLines(textLines)
    cowStr = '\n' + '\n'.join(bubbleLines) + COW
    return cowStr


def getTextLines(text):
    maxCharsPerLine = 39
    lines = []

    # get leading whitespace, middle tokens, and trailing whitespace
    tokens = [''] * (text[0] == ' ')
    tokens.extend(text.split())
    tokens.extend([''] * (len(text) > 1 and text[-1] == ' '))

    for token in tokens:
        if not lines or len(lines[-1]) == maxCharsPerLine:
            lines.append('')

        needSpace = lines[-1] and lines[-1][-1] != ' ' or not token

        lineLenWithToken = len(lines[-1]) + needSpace + len(token)

        # if token will fit on line
        if lineLenWithToken <= maxCharsPerLine:
            lines[-1] += ' ' * needSpace + token
        # else token won't fit on this line
        else:
            while token:
                if lines[-1]:
                    lines.append('')

                lines[-1] += token[:maxCharsPerLine]
                token = token[maxCharsPerLine:]

    return lines


def getBubbleLines(textLines):
    maxTextLineLen = max(map(len, textLines))

    bubbleLines = [' ' + '_' * (maxTextLineLen + 2)]

    for lineIdx, textLine in enumerate(textLines):
        if len(textLines) == 1:
            leftBorder = '< '
            rightBorder = ' >'
        elif lineIdx == 0:
            leftBorder = '/ '
            rightBorder = ' \\'
        elif lineIdx == len(textLines) - 1:
            leftBorder = '\\ '
            rightBorder = ' /'
        else:
            leftBorder = '| '
            rightBorder = ' |'

        spacePadding = ' ' * (maxTextLineLen - len(textLine))
        bubbleLines.append(leftBorder + textLine + spacePadding + rightBorder)

    bubbleLines.append(' ' + '-' * (maxTextLineLen + 2))

    return bubbleLines


if __name__ == '__main__':
    expected_cowsay_one_line = r'''
 ________________
< Checkio rulezz >
 ----------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
'''
    expected_cowsay_two_lines = r'''
 ________________________________________
/ A                                      \
\ longtextwithonlyonespacetofittwolines. /
 ----------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
'''

    expected_cowsay_many_lines = r'''
 _________________________________________
/ Lorem ipsum dolor sit amet, consectetur \
| adipisicing elit, sed do eiusmod tempor |
| incididunt ut labore et dolore magna    |
\ aliqua.                                 /
 -----------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
'''

    base_in_long_without_spaces_two_lines = 'looooooooooooooooooooooooooooooooooooong'
    base_out_long_without_spaces_two_lines = r'''
 _________________________________________
/ looooooooooooooooooooooooooooooooooooon \
\ g                                       /
 -----------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
'''


    in_space_a = ' a'
    expected_space_a = r'''
 ____
<  a >
 ----
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
'''


    cowsay_one_line = cowsay('Checkio rulezz')
    assert cowsay_one_line == expected_cowsay_one_line, 'Wrong answer:\n%s' % cowsay_one_line

    cowsay_two_lines = cowsay('A longtextwithonlyonespacetofittwolines.')
    assert cowsay_two_lines == expected_cowsay_two_lines, 'Wrong answer:\n%s' % cowsay_two_lines

    cowsay_many_lines = cowsay(
        'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do '
        'eiusmod tempor incididunt ut labore et dolore magna aliqua.')
    assert cowsay_many_lines == expected_cowsay_many_lines, 'Wrong answer:\n%s' % cowsay_many_lines

    long1 = cowsay(base_in_long_without_spaces_two_lines)
    assert long1 == base_out_long_without_spaces_two_lines, 'Wrong answer:\n%s' % long1

    out_space_a = cowsay(in_space_a)
    assert out_space_a == expected_space_a, 'Wrong answer:\n%s' % long1

