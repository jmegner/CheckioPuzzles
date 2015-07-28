'''
author: Jacob Egner
date: 2015-07-27
island: elementary

puzzle prompt and puzzle prompt source repo:
http://www.checkio.org/mission/secret-message/
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-secret-message

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


def find_message(text):
    return ''.join(letter for letter in text if letter.isupper())


if __name__ == '__main__':
    assert find_message("How are you? Eh, ok. Low or Lower? Ohhh.") == "HELLO", "hello"
    assert find_message("hello world!") == "", "Nothing"
    assert find_message("HELLO WORLD!!!") == "HELLOWORLD", "Capitals"


