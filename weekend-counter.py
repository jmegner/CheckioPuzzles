'''
author: Jacob Egner
date: 2015-07-29
island: scientific expedition

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


from datetime import date, timedelta


def checkio(dateBegin, dateEnd):
    dateCurr = dateBegin
    numRestDays = 0

    while dateCurr <= dateEnd:
        if dateCurr.isoweekday() >= 6:
            numRestDays += 1

        dateCurr += timedelta(1)

    return numRestDays


if __name__ == '__main__':
    assert checkio(date(2013, 9, 18), date(2013, 9, 23)) == 2, "1st example"
    assert checkio(date(2013, 1, 1), date(2013, 2, 1)) == 8, "2nd example"
    assert checkio(date(2013, 2, 2), date(2013, 2, 3)) == 2, "3rd example"


