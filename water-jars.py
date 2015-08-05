'''
author: Jacob Egner
date: 2015-08-04
island: ice base

puzzle URLs:
http://www.checkio.org/mission/water-jars/
https://github.com/Bryukh-Checkio-Tasks/checkio-task-water-jars

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

note: this file contains three alternative solutions
    1: efficient iterative breadth first search
    2: inefficient recursive depth first search
    3: fun iterative algo that does not necessarily find minimal steps
'''


import collections
import itertools


################################################################################
# efficient iterative breadth first search approach

class Jar(collections.namedtuple("Jar", ["name", "volume", "water"])):

    def isEmpty(self):  return self.water == 0
    def isFull(self):   return self.water == self.volume
    def asEmpty(self):  return Jar(self.name, self.volume, 0)
    def asFull(self):   return Jar(self.name, self.volume, self.volume)
    def fillStr(self):  return "0" + self.name
    def drainStr(self): return self.name + "0"
    def transferStr(self, other): return self.name + other.name


    def withWaterChange(self, waterChange):
        return Jar(self.name, self.volume, self.water + waterChange)


class State(collections.namedtuple("State", ["jar1", "jar2", "steps"])):

    def meetsGoal(self, goal):
        return self.jar1.water == goal or self.jar2.water == goal


def checkio(volume1, volume2, goal):
    '''efficient breadth first search for minimal steps'''
    initialJar1 = Jar("1", volume1, 0)
    initialJar2 = Jar("2", volume2, 0)

    states = [State(initialJar1, initialJar2, [])]

    while True:
        nextStates = []

        for state in states:
            prevStep = state.steps[-1] if state.steps else ""

            for jarA, jarB in itertools.permutations((state.jar1, state.jar2)):

                # if reasonable to fill jarA
                if not jarA.isFull() and prevStep != jarA.drainStr():
                    newState = State(
                        jarA.asFull(),
                        jarB,
                        state.steps + [jarA.fillStr()])

                    if newState.meetsGoal(goal):
                        return newState.steps

                    nextStates.append(newState)

                # if reasonable to drain jarA
                if jarA.water and prevStep != jarA.fillStr():
                    newState = State(
                        jarA.asEmpty(),
                        jarB,
                        state.steps + [jarA.drainStr()])

                    if newState.meetsGoal(goal):
                        return newState.steps

                    nextStates.append(newState)

                # if reasonable to pour water from jarA to jarB
                if(jarA.water and not jarB.isFull()
                    and prevStep != jarB.transferStr(jarA)
                ):
                    transferAmount = min(jarA.water, jarB.volume - jarB.water)
                    newState = State(
                        jarA.withWaterChange(-transferAmount),
                        jarB.withWaterChange(+transferAmount),
                        state.steps + [jarA.transferStr(jarB)])

                    if newState.meetsGoal(goal):
                        return newState.steps

                    nextStates.append(newState)

        states = nextStates


################################################################################
# inefficient recursive depth first search approach

def checkioDepthFirstRecursive(volume1, volume2, goal):
    steps = depthFirstSearch(
        goal,
        Jar("1", volume1, 0),
        Jar("2", volume2, 0),
        [],
        {},
    )

    return steps


def depthFirstSearch(goal, jar1, jar2, steps, situationToNumSteps):
    situation = tuple(sorted((jar1, jar2)))

    if(situation in situationToNumSteps
        and situationToNumSteps[situation] <= len(steps)
    ):
        return []

    situationToNumSteps[situation] = len(steps)

    if jar1.water == goal or jar2.water == goal:
        return steps

    stepBranches = []

    for jarA, jarB in [(jar1, jar2), (jar2, jar1)]:
        # if reasonable to fill jarA
        if jarA.water < jarA.volume:
            stepBranches.append(depthFirstSearch(
                goal,
                jarA.asFull(),
                jarB,
                steps + [jarA.fillStr()],
                situationToNumSteps,
            ))

        # if reasonable to drain jarA
        if jarA.water:
            stepBranches.append(depthFirstSearch(
                goal,
                jarA.asEmpty(),
                jarB,
                steps + [jarA.drainStr()],
                situationToNumSteps,
            ))

        # if reasonable to pour from jarA to jarB
        if jarA.water and jarB.water < jarB.volume:
            transferAmount = min(jarA.water, jarB.volume - jarB.water)
            stepBranches.append(depthFirstSearch(
                goal,
                jarA.withWaterChange(-transferAmount),
                jarB.withWaterChange(+transferAmount),
                steps + [jarA.transferStr(jarB)],
                situationToNumSteps,
            ))

    sortedStepBranches = sorted(
        [branch for branch in stepBranches if branch],
        key = len)

    if sortedStepBranches:
        return sortedStepBranches[0]

    return []


################################################################################
# fun iterative algo that does not necessarily find minimal step sequence

class FunJar:

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


def checkioNonMinimal(jar1Volume, jar2Volume, goal):
    if jar1Volume < jar2Volume:
        smallJar = FunJar("1", jar1Volume)
        bigJar = FunJar("2", jar2Volume)
    else:
        smallJar = FunJar("2", jar2Volume)
        bigJar = FunJar("1", jar1Volume)

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


################################################################################
# self-checking

if __name__ == '__main__':
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

