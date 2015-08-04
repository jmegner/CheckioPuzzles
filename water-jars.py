'''
author: Jacob Egner
date: 2015-08-04
island: ice base

puzzle URLs:
http://www.checkio.org/mission/water-jars/
https://github.com/Bryukh-Checkio-Tasks/checkio-task-water-jars

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles
'''


class Jar:

    def __init__(self, name, volume):
        self.name = name
        self.volume = volume
        self.water = 0


    def fill(self):
        self.water = self.volume
        return "0" + self.name


    def drain(self):
        self.water = 0
        return self.name + "0"


    def transfer(self, other):
        otherRemainingCapacity = other.volume - other.water
        transferAmount = min(otherRemainingCapacity, self.water)

        self.water -= transferAmount
        other.water += transferAmount

        return self.name + other.name


def checkio(jar1Volume, jar2Volume, goal):
    if jar1Volume < jar2Volume:
        smallJar = Jar("1", jar1Volume)
        bigJar = Jar("2", jar2Volume)
    else:
        smallJar = Jar("2", jar2Volume)
        bigJar = Jar("1", jar1Volume)

    steps = []

    while True:
        steps.append(bigJar.fill())
        steps.append(bigJar.transfer(smallJar))

        if bigJar.water == goal or smallJar.water == goal:
            return steps

        while bigJar.water:
            steps.append(smallJar.drain())
            steps.append(bigJar.transfer(smallJar))

            if bigJar.water == goal or smallJar.water == goal:
                return steps

    return None


if __name__ == '__main__':
    #This part is using only for self-checking and not necessary for auto-testing
    def check_solution(func, initial_data, max_steps):
        first_volume, second_volume, goal = initial_data
        actions = {
            "01": lambda f, s: (first_volume, s),
            "02": lambda f, s: (f, second_volume),
            "12": lambda f, s: (
                f - (second_volume - s if f > second_volume - s else f),
                second_volume if f > second_volume - s else s + f),
            "21": lambda f, s: (
                first_volume if s > first_volume - f else s + f,
                s - (first_volume - f if s > first_volume - f else s),
            ),
            "10": lambda f, s: (0, s),
            "20": lambda f, s: (f, 0)
        }
        first, second = 0, 0
        result = func(*initial_data)
        if len(result) > max_steps:
            print("You answer contains too many steps. It can be shorter.")
            return False
        for act in result:
            if act not in actions.keys():
                print("I don't know this action {0}".format(act))
                return False
            first, second = actions[act](first, second)
        if goal == first or goal == second:
            return True
        print("You did not reach the goal.")
        return False

    assert check_solution(checkio, (5, 7, 6), 10), "Example"
    assert check_solution(checkio, (3, 4, 1), 2), "One and two"
