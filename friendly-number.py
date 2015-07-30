'''
author: Jacob Egner
date: 2015-07-30
island: scientific expedition

puzzle URLs:
http://www.checkio.org/mission/friendly-number/
https://github.com/Bryukh-Checkio-Tasks/checkio-task-friendly-number

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


import decimal


def friendly_number(
    number,
    base=1000,
    decimals=0,
    suffix='',
    powers=['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
):
    number = decimal.Decimal(number)
    basePower = 0

    while abs(number) >= base and basePower < len(powers) - 1:
        number /= base
        basePower += 1

    # round down when no decimals
    if decimals == 0:
        number = int(number)

    return "{:.{}f}{}{}".format(
        number,
        decimals,
        powers[basePower],
        suffix,
    )


if __name__ == '__main__':
    assert friendly_number(102) == '102', '102'
    assert friendly_number(10240) == '10k', '10k'
    assert friendly_number(12341234, decimals=1) == '12.3M', '12.3M'
    assert friendly_number(12461, decimals=1) == '12.5k', '12.5k'
    assert friendly_number(1024000000, base=1024, suffix='iB') == '976MiB', '976MiB'

    assert friendly_number(-150, base=100, powers=["","d","D"]
        ) == '-1d', '-1d, test_base_7'

    assert friendly_number(10**32) == '100000000Y', 'test_edges_4'


