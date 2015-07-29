'''
author: Jacob Egner
date: 2015-07-29
island: scientific expedition

puzzle URLs:
http://www.checkio.org/mission/digit-stack/
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-digit-stack

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


def digit_stack(commands):
    valStack = []
    valSum = 0

    for command in commands:
        tokens = command.split(' ')

        if tokens[0] == "PUSH":
            valStack.append(int(tokens[1]))
        elif tokens[0] == "POP":
            if valStack:
                valSum += valStack.pop()
        elif tokens[0] == "PEEK":
            if valStack:
                valSum += valStack[-1]
        else:
            raise ValueError("unrecognized command")

    return valSum


if __name__ == '__main__':
    assert digit_stack([
        "PUSH 3", "POP", "POP", "PUSH 4", "PEEK",
        "PUSH 9", "PUSH 0", "PEEK", "POP", "PUSH 1", "PEEK"
        ]) == 8, "Example"
    assert digit_stack(["POP", "POP"]) == 0, "pop, pop, zero"
    assert digit_stack(["PUSH 9", "PUSH 9", "POP"]) == 9, "Push the button"
    assert digit_stack([]) == 0, "Nothing"


