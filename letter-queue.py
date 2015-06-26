import collections


def letter_queue(commands):
    letters = collections.deque()

    for command in commands:
        args = command.split(' ')

        if args[0] == "POP":
            if letters:
                letters.popleft()
        else:
            letters.append(args[1])

    return ''.join(letters)


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert letter_queue(["PUSH A", "POP", "POP", "PUSH Z", "PUSH D", "PUSH O", "POP", "PUSH T"]) == "DOT", "dot example"
    assert letter_queue(["POP", "POP"]) == "", "Pop, Pop, empty"
    assert letter_queue(["PUSH H", "PUSH I"]) == "HI", "Hi!"
    assert letter_queue([]) == "", "Nothing"
