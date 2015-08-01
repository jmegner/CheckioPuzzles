'''
author: Jacob Egner
date: 2015-08-01
island: electronic station

puzzle URLs:
http://www.checkio.org/mission/mind-switcher/
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-mind-switcher

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

overview:
my solution is based off the steps stated at:
http://theinfosphere.org/Futurama_theorem

But I have reversed diretion and processing of the lines.

Step 1: Have everybody who's messed up arrange themselves in circles, each
    facing the body their mind should land in (e.g., if Fry's mind is in
    Zoidberg's body, then the Zoidberg body should face the Fry body).

Step 2: Go get two "fresh" (as of yet never mind-swapped) people. Let's call
    them Helper A and Helper B.

Step 3: Fix the circles one by one as follows:

    3.0: Start each time with Helper A and Helper B's minds in either their own
        or each other's bodies

    3.1: Pick any circle of messed-up people you like and unwrap it into a line
        with whoever you like at the front

    3.2: Swap the mind at the back of the line into Helper A's body

    3.3: From front to back, have everybody in the line swap minds with
        Helper B's body in turn. (This moves each mind in the line, apart from
        the back one, backward into the right body)

    3.4: Swap the mind in Helper A's body back where it belongs, into the body
        at the front of the line. Now the circle/line has been completely fixed.
        The one side effect is that for each time a circle is fixed, the
        Helpers' minds will switch places, but that's OK, see below

Step 4: At the very end, after all the circles have been fixed, mind-swap the
    two Helpers if necessary (i.e., in case there was originally an odd number
    of messed-up circles)
'''


def mind_switcher(journal):
    bodyToMind = getBodyToMind(journal)
    cycles = getCycles(bodyToMind)
    neededSwaps = getNeededSwaps(cycles)

    return neededSwaps


def getBodyToMind(journal):
    bodyToMind = {}

    for body1, body2 in journal:
        if body1 not in bodyToMind:
            bodyToMind[body1] = body1
        if body2 not in bodyToMind:
            bodyToMind[body2] = body2

        bodyToMind[body1], bodyToMind[body2] = (
            bodyToMind[body2], bodyToMind[body1])

    return bodyToMind


def getCycles(bodyToMind):
    cycles = []
    bodysToCycle = set(bodyToMind.keys())

    while bodysToCycle:
        cycles.append([bodysToCycle.pop()])

        while True:
            nextBody = bodyToMind[cycles[-1][-1]]

            if nextBody == cycles[-1][0]:
                # no need to track or correct cycles of one
                if len(cycles[-1]) == 1:
                    cycles.pop()
                break

            cycles[-1].append(nextBody)
            bodysToCycle.remove(nextBody)

    return cycles


def getNeededSwaps(cycles):
    helperA = "nikola"
    helperB = "sophia"
    neededSwaps = []

    for cycle in cycles:
        neededSwaps.append({helperA, cycle[-1]})

        for body in cycle:
            neededSwaps.append({helperB, body})

        neededSwaps.append({helperA, cycle[0]})

    if len(cycles) % 2 == 1:
        neededSwaps.append({helperA, helperB})

    return neededSwaps


if __name__ == '__main__':
    def check_solution(func, data):
        robots = {"nikola": "nikola", "sophia": "sophia"}
        switched = []
        for pair in data:
            switched.append(set(pair))
            r1, r2 = pair
            robots[r1], robots[r2] = robots.get(r2, r2), robots.get(r1, r1)

        result = func(data)
        if not isinstance(result, (list, tuple)) or not all(isinstance(p, set) for p in result):
            print("The result should be a list/tuple of sets.")
            return False
        for pair in result:
            if len(pair) != 2:
                print(1, "Each pair should contain exactly two names.")
                return False
            r1, r2 = pair
            if not isinstance(r1, str) or not isinstance(r2, str):
                print("Names must be strings.")
                return False
            if r1 not in robots.keys():
                print("I don't know '{}'.".format(r1))
                return False
            if r2 not in robots.keys():
                print("I don't know '{}'.".format(r2))
                return False
            if set(pair) in switched:
                print("'{}' and '{}' already were switched.".format(r1, r2))
                return False
            switched.append(set(pair))
            robots[r1], robots[r2] = robots[r2], robots[r1]
        for body, mind in robots.items():
            if body != mind:
                print("'{}' has '{}' mind.".format(body, mind))
                return False
        return True

    assert check_solution(mind_switcher, (
        {"scout", "super"},))

    assert check_solution(mind_switcher, (
        {'hater', 'scout'}, {'planer', 'hater'}))

    assert check_solution(mind_switcher, (
        {'scout', 'driller'}, {'scout', 'lister'}, {'hater', 'digger'},
        {'planer', 'lister'}, {'super', 'melter'}))

    # test 3
    assert check_solution(mind_switcher, (
        {"digger", "melter"}, {"melter", "planer"}, {"digger", "planer"},))

