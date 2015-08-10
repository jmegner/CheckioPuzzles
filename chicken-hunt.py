'''
author: Jacob Egner
date: 2015-08-10
island: ice base

puzzle URLs:
http://www.checkio.org/mission/chicken-hunt/
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-chicken-hunt

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles
'''


import math
import random


DIRS = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1),
    "NW": (-1, -1),
    "NE": (-1, 1),
    "SE": (1, 1),
    "SW": (1, -1),
    "": (0, 0),
}

HOBBIT_SELF = "I"
HOBBIT_OTHER = "S"
CHICKEN = "C"


def hunt(yard):
    myLoc = findChar(yard, HOBBIT_SELF)
    partnerLoc = findChar(yard, HOBBIT_OTHER)

    if myLoc < partnerLoc:
        return ""

    chickenLoc = findChar(yard, CHICKEN)
    adjDirsAndLocs = findFreeAdjacent(yard, myLoc)

    myNextDirAndLoc = min(adjDirsAndLocs, key = lambda dirAndLoc: math.hypot(
        dirAndLoc[1][0] - chickenLoc[0], dirAndLoc[1][1] - chickenLoc[1])
    )

    return myNextDirAndLoc[0]


def findChar(yard, symb):
    for i, row in enumerate(yard):
        for j, ch in enumerate(row):
            if ch == symb:
                return i, j
    return None, None


def findFreeAdjacent(yard, position):
    x, y = position
    result = [("", position)]
    for k, (dx, dy) in DIRS.items():
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(yard) and 0 <= ny < len(yard[0]) and yard[nx][ny] == ".":
            result.append((k, (nx, ny)))
    return result


if __name__ == "__main__":
    # These checker is using only for your local testing
    # It's run function in the same environment, but in the grading it will be in various
    from random import choice
    from re import sub
    from math import hypot

    def random_chicken(_, possible):
        return choice(possible)


    def distance_chicken(func):
        def run_chicken(yard, possible):
            enemies = [find_position(yard, str(i + 1)) for i in range(N)]
            best = "", find_position(yard, "C")
            best_dist = 0 if func == max else float("inf")
            for d, (x, y) in possible:
                min_dist = min(hypot(x - ex, y - ey) for ex, ey in enemies)
                if func(min_dist, best_dist) == min_dist:
                    best = d, (x, y)
                    best_dist = min_dist
                elif min_dist == best_dist:
                    best = choice([(d, (x, y)), best])
                #print(best, best_dist)
            return best

        return run_chicken


    CHICKEN_ALGORITHM = {
        "random": random_chicken,
        "run_away": distance_chicken(max),
        "hunter": distance_chicken(min)
    }

    ERROR_TYPE = "Your function must return a direction as a string."
    ERROR_FENCE = "A hobbit struck in the fence."
    ERROR_TREE = "A hobbit struck in an obstacle."
    ERROR_HOBBITS = "The Hobbits struck each other."
    ERROR_TIRED = "The Hobbits are tired."

    N = 2

    MAX_STEP = 100

    def find_position(yard, symb):
        for i, row in enumerate(yard):
            for j, ch in enumerate(row):
                if ch == symb:
                    return i, j
        return None, None

    def find_free(yard, position):
        x, y = position
        result = [("", position)]
        for k, (dx, dy) in DIRS.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(yard) and 0 <= ny < len(yard[0]) and yard[nx][ny] == ".":
                result.append((k, (nx, ny)))
        return result

    def prepare_yard(yard, numb):
        return tuple(sub("\d", "S", row.replace(str(numb), "I")) for row in yard)

    def checker(func, yard, chicken_algorithm="random"):
        for _ in range(MAX_STEP):
            individual_yards = [prepare_yard(yard, i + 1) for i in range(N)]
            results = [func(y) for y in individual_yards]
            if any(not isinstance(r, str) or r not in DIRS.keys() for r in results):
                print(ERROR_TYPE)
                return False
            chicken = find_position(yard, "C")
            possibles = find_free(yard, chicken)
            chicken_action, new_chicken = CHICKEN_ALGORITHM[chicken_algorithm](yard, possibles)
            positions = [find_position(yard, str(i + 1)) for i in range(N)]
            new_positions = []
            for i, (x, y) in enumerate(positions):
                nx, ny = x + DIRS[results[i]][0], y + DIRS[results[i]][1]
                if not (0 <= nx < len(yard) and 0 <= ny < len(yard[0])):
                    print(ERROR_FENCE)
                    return False
                if yard[nx][ny] == "X":
                    print(ERROR_TREE)
                    return False
                new_positions.append((nx, ny))
            if len(set(new_positions)) != len(new_positions):
                print(ERROR_HOBBITS)
                return False

            if any(new_chicken == pos for pos in new_positions):
                print("Gratz!")
                return True

            # update yard
            temp_yard = [[ch if ch in ".X" else "." for ch in row] for row in yard]
            for i, (x, y) in enumerate(new_positions):
                temp_yard[x][y] = str(i + 1)
            temp_yard[new_chicken[0]][new_chicken[1]] = "C"
            yard = tuple("".join(row) for row in temp_yard)
        print(ERROR_TIRED)
        return False

    assert checker(hunt, (
        "......",
        ".1.XX.",
        "...CX.",
        ".XX.X.",
        "...2..",
        "......",
        ), "random"), "Example 1"

    assert checker(hunt, (
        "......",
        ".1.XX.",
        "...CX.",
        ".XX.X.",
        "...2..",
        "......",
        ), "run_away"), "Example 1"

    assert checker(hunt, (
        "......",
        ".1.XX.",
        "...CX.",
        ".XX.X.",
        "...2..",
        "......",
        ), "hunter"), "Example 1"

    assert checker(hunt, (
        "1.........",
        ".X.X.X.X.X",
        ".X.X.X.X.X",
        ".X.X.X.X.X",
        ".X.X.X.X.X",
        ".X.XCX.X.X",
        ".X.X.X.X.X",
        ".X.X.X.X.X",
        ".X.X.X.X.X",
        ".X.X.X.X.X",
        ".........2",
        ), "run_away"), "Tunnels"

    assert checker(hunt, (
        "1X.X.X.X2",
        "X.X.X.X.X",
        ".X.X.X.X.",
        "X.X.X.X.X",
        ".X.X.X.X.",
        "X.X.X.X.X",
        ".X.XCX.X.",
        "X.X.X.X.X",
        )), "ChessBoard"

    assert checker(hunt, (
        "...2...",
        ".......",
        ".......",
        "...C...",
        ".......",
        ".......",
        "...1...",
        ), "random"), "Clear Random"

    assert checker(hunt, (
        "...2...",
        ".......",
        ".......",
        "...C...",
        ".......",
        ".......",
        "...1...",
        ), "run_away"), "Clear Away"

    assert checker(hunt, (
        "...2...",
        ".......",
        ".......",
        "...C...",
        ".......",
        ".......",
        "...1...",
        ), "hunter"), "Clear Hunter"

    assert checker(hunt, (
            "..1..X..",
            ".X.XXX..",
            "....X...",
            ".X.XXX..",
            "..X..X..",
            "X..XC.X.",
            "....XX..",
            "..X..X..",
            "X..X2...",
        ), "random"), "Chaos Random"

    assert checker(hunt, (
            "..1..X..",
            ".X.XXX..",
            "....X...",
            ".X.XXX..",
            "..X..X..",
            "X..XC.X.",
            "....XX..",
            "..X..X..",
            "X..X2...",
        ), "hunter"), "Chaos Hunter"

    assert checker(hunt, (
            ".........",
            ".XXXXXXX.",
            ".X.....X.",
            ".X.XXXCX.",
            ".X2....X.",
            ".X1XXXXX.",
            ".X.......",
            ".XXXXXXX.",
            ".........",
        ), "run_away"), "Running Away"

    assert checker(hunt, (
            ".......",
            ".XXXXX.",
            ".X1.2X.",
            ".X...X.",
            ".X...X.",
            ".XX.XX.",
            "C......",
        ), "run_away"), "Passage Away"

    assert checker(hunt, (
            ".XXX.",
            ".X1X.",
            ".XCX.",
            ".X2X.",
            ".XXX.",
        ), "random"), "Be Calm Random"

    assert checker(hunt, (
            "..........",
            ".XXXXXXXX.",
            ".X.X....2.",
            ".X...XXXX.",
            ".X.X.X.1X.",
            ".X.X.X..X.",
            ".X.X.XX.X.",
            ".X.XX...X.",
            ".XXCXXXXX.",
            "..........",
        ), "random"), "Maze random"

    assert checker(hunt, (
            "..........",
            ".XXXXXXXX.",
            ".X.X....2.",
            ".X...XXXX.",
            ".X.X.X.1X.",
            ".X.X.X..X.",
            ".X.X.XX.X.",
            ".X.XX...X.",
            ".XXCXXXXX.",
            "..........",
        ), "run_away"), "Maze away"

    assert checker(hunt, (
            "..........",
            ".XXXXXXXX.",
            ".X.X....2.",
            ".X...XXXX.",
            ".X.X.X.1X.",
            ".X.X.X..X.",
            ".X.X.XX.X.",
            ".X.XX...X.",
            ".XXCXXXXX.",
            "..........",
        ), "hunter"), "Maze hunter"

    assert checker(hunt, (
            "....C....",
            ".XXX.XXX.",
            ".X1XXX2X.",
            ".XX.X.XX.",
            ".XXX.XXX.",
            "...X.X...",
            "...X.X...",
            ".........",
        ), "random"), "hangover random"

