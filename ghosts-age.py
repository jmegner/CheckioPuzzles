def checkio(opacity):
    # print("opacity={}".format(opacity))
    age = 0
    simOpacity = 10000
    fibos = [0, 1]

    while simOpacity != opacity and age < 5000:
        age += 1

        while fibos[-1] < age:
            fibos.append(fibos[-1] + fibos[-2])

        if age == fibos[-1]:
            simOpacity -= age
        else:
            simOpacity += 1

        # print("  age={}, simOpacity={}, fibos={}".format(
        #     age, simOpacity, fibos))

    return age


#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio(10000) == 0, "Newborn"
    assert checkio(9999) == 1, "1 year"
    assert checkio(9997) == 2, "2 years"
    assert checkio(9994) == 3, "3 years"
    assert checkio(9995) == 4, "4 years"
    assert checkio(9990) == 5, "5 years"
