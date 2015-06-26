FIRST_TEN = ["ERROR1", "one", "two", "three", "four", "five", "six", "seven",
             "eight", "nine"]
SECOND_TEN = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
              "sixteen", "seventeen", "eighteen", "nineteen"]
OTHER_TENS = ["ERROR2", "ERROR3", "twenty", "thirty", "forty", "fifty",
    "sixty", "seventy", "eighty", "ninety"]
HUNDRED = "hundred"


def checkio(number):
    english = ""

    hundreds = (number % 1000) // 100

    if hundreds:
        english += "{} {} ".format(FIRST_TEN[hundreds], HUNDRED)

    tens = (number % 100) // 10
    ones = number % 10

    if tens == 1:
        english += SECOND_TEN[ones] + " "
    else:
        if tens:
            english += OTHER_TENS[tens] + " "
        if ones:
            english += FIRST_TEN[ones] + " "

    if english[-1] == " ":
        english = english[:-1]

    return english


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert checkio(4) == 'four', "1st example"
    assert checkio(133) == 'one hundred thirty three', "2nd example"
    assert checkio(12) == 'twelve', "3rd example"
    assert checkio(101) == 'one hundred one', "4th example"
    assert checkio(212) == 'two hundred twelve', "5th example"
    assert checkio(40) == 'forty', "6th example"
    assert not checkio(212).endswith(' '), "Don't forget strip whitespaces at the end of string"
