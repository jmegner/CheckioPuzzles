def checkio(expression):
    endBracketToBeginBracket = {
        ')' : '(',
        ']' : '[',
        '}' : '{',
        }
    bracketChars = '()[]{}'
    bracketStack = []

    for char in expression:
        if char in bracketChars:
            # if begin bracket
            if char in endBracketToBeginBracket.values():
                # then always accept and put on stack
                bracketStack.append(char)
            # else end bracket
            else:
                # end bracket must be preceded by matching begin bracket
                if (not bracketStack or bracketStack[-1]
                        != endBracketToBeginBracket[char]):
                    return False
                else:
                    bracketStack.pop()

    return not bracketStack

#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio("((5+3)*2+1)") == True, "Simple"
    assert checkio("{[(3+1)+2]+}") == True, "Different types"
    assert checkio("(3+{1-1)}") == False, ") is alone inside {}"
    assert checkio("[1+1]+(2*2)-{3/3}") == True, "Different operators"
    assert checkio("(({[(((1)-2)+3)-3]/3}-3)") == False, "One is redundant"
    assert checkio("2+3") == True, "No brackets, no problem"
