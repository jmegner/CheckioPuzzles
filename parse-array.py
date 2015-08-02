'''
author: Jacob Egner
date: 2015-08-01
island: electronic station

puzzle URLs:
http://www.checkio.org/mission/parse-array/
https://github.com/Bryukh-Checkio-Tasks/parse-array

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

note: this is a "fix the bug in pre-existing code" type puzzle;
note: puzzle forbids import, exec, and eval
'''


WHITESPACE_STR = ' \t\n\r'


def parse_array(s, _w=WHITESPACE_STR, _sep=","):
    array = None
    stack = []
    accumulator = ""
    closed_flag = False
    sep_flag = False
    whitespace_flag = False
    started_flag = False
    for ch in s:
        if ch in _w:
            whitespace_flag = True
            continue
        if ch == "[":
            if started_flag and not stack:
                raise ValueError("Wrong string.")
            if closed_flag or accumulator:
                raise ValueError
            in_array = []
            if stack:
                stack[-1](in_array)
            else:
                array = in_array
                started_flag = True
            stack.append(in_array.append)
        elif not started_flag:
            raise ValueError("Wrong string.")
        elif ch == "]":

            if not stack:
                raise ValueError("Wrong string.")
            if accumulator:
                stack[-1](int(accumulator))
                accumulator = ""
            stack.pop()
            closed_flag = True
            sep_flag = False
            whitespace_flag = False
        elif ch in _sep:
            # START OF MODIFICATION 2
            # modification needed to handle "[3],"
            if not stack:
                raise ValueError("separator outside of all braces.")
            # END OF MODIFICATION 2
            if accumulator:
                stack[-1](int(accumulator))
                accumulator = ""
            elif closed_flag:
                pass
            else:
                raise ValueError("Wrong string.")
            sep_flag = True
            closed_flag = False
            whitespace_flag = False
        else:
            if whitespace_flag and accumulator or closed_flag:
                raise ValueError
            accumulator += ch
        whitespace_flag = False
    if not array is None:
        # START OF MODIFICATION 1
        # modification needed to handle "[[2]"
        if stack:
            raise ValueError("not enough closing braces")
        # END OF MODIFICATION 1
        return array
    else:
        raise ValueError("Wrong string")


if __name__ == "__main__":
    assert parse_array("[1, 2, 3]") == [1, 2, 3], "Simple"
    assert parse_array("[[1], 2, 3]") == [[1], 2, 3], "Nested"
    assert parse_array("[-3, [-2, 0], 10]") == [-3, [-2, 0], 10], "Negative integers"
    assert parse_array("[100]") == [100], "One number"
    assert parse_array("[2,     3]") == [2, 3], "Whitespaces"
    assert parse_array("[[10, [11]], [[[1], 2], 3], 5]") == [[10, [11]], [[[1], 2], 3], 5], "Deep nested"
    assert parse_array("   [3, 4]   ") == [3, 4], "Skip whitespaces"
    assert parse_array("[[], 0]") == [[], 0], "Empty arrays"
    assert parse_array("[[0,], 0]") == [[0], 0], "Comma - closed bracket"

    try:
        parse_array("[asd]")
        assert False, "Only integers"
    except ValueError:
        pass

    try:
        parse_array("[2, 3]]")
        assert False, "Excess bracket"
    except ValueError:
        pass

    try:
        parse_array("[++2, 1]")
        assert False, "Two plus"
    except ValueError:
        pass

    try:
        parse_array("[10, 11, , 12]")
        assert False, "Two separators"
    except ValueError:
        pass

    try:
        parse_array(" 13 ")
        assert False, "Where is a list?"
    except ValueError:
        pass

    try:
        parse_array("[[2]")
        assert False, "Excess opened bracket"
    except ValueError:
        pass

    try:
        parse_array("[3 4]")
        assert False, "Check for spurious spaces within a number"
    except ValueError:
        pass

    try:
        parse_array("[10, 11,, 12]")
        assert False, "Check for double separators without a space in between"
    except ValueError:
        pass

    try:
        parse_array("[[]3]")
        assert False, "Check for missing separators after []"
    except ValueError:
        pass

    try:
        parse_array("[2[]]")
        assert False, " Check for missing separators before []"
    except ValueError:
        pass

    try:
        parse_array("[3],")
        assert False, "Excess separator"
    except ValueError:
        pass

    try:
        parse_array("[1,2]3")
        assert False, "Excess number"
    except ValueError:
        pass

    try:
        parse_array("[1], [2,3]")
        assert False, "Here should be only one array."
    except ValueError:
        pass

