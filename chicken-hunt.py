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


import collections
import itertools
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

class Misc:
    s_hobbitSelf = "I"
    s_hobbitOther = "S"
    s_chicken = "C"
    s_open = "."
    s_wall = "X"


class Loc(collections.namedtuple('Loc', ['r', 'c'])):

    def __neg__(self): return Loc(-self.r, -self.c)
    def __add__(self, other): return Loc(self.r + other.r, self.c + other.c)
    def __sub__(self, other): return self + -other
    def __mul__(self, scale): return Loc(self.r * scale, self.c * scale)

    def getVal(self, grid): return grid[self.r][self.c]
    def setVal(self, grid, val): grid[self.r][self.c] = val

    def inBounds(self, grid):
        return ( self.r >= 0 and self.c >= 0
            and self.r < len(grid)
            and self.c < len(grid[self.r]) )

    def euclidDist(self, other):
        return math.hypot(self.r - other.r, self.c - other.c)

    def principalNeighbors(
        self,
        grid=None,
        onlyIncludeOpenOrSelf=False,
    ):
        neighbors = []

        for delta in Loc.s_principalDels.keys():
            newLoc = self + delta

            if grid is None or newLoc.inBounds(grid):
                if newLoc.getVal(grid) == Misc.s_wall:
                    continue

                isSelf = delta == Loc(0, 0)
                isOpen = newLoc.getVal(grid) == Misc.s_open

                if isSelf or isOpen or not onlyIncludeOpenOrSelf:
                    neighbors.append(newLoc)

        return neighbors


Loc.s_principalDels = collections.OrderedDict([
    (Loc(-1, +0), 'N'),
    (Loc(-1, +1), 'NE'),
    (Loc(+0, +1), 'E'),
    (Loc(+1, +1), 'SE'),
    (Loc(+1, +0), 'S'),
    (Loc(+1, -1), 'SW'),
    (Loc(+0, -1), 'W'),
    (Loc(-1, -1), 'NW'),
    (Loc(+0, +0), ''),
])


class YardNode(collections.namedtuple(
    'YardNode',
    ['yard', 'chickenLoc', 'hobALoc', 'hobBLoc',])
):
    pass

class YardExtra(collections.namedtuple(
    'YardExtra',
    ['stepNum', 'goodChildNode']
):
    pass


class HobbitNode(collections.namedtuple(
    'HobbitNode',
    ['hobALoc', 'hobBLoc', 'possibleYardNodes']
):
    pass


g_algoRandom = "random"
g_algoAway = "run_away"
g_algoHunter = "hunter"
g_allPossibleChickenAlgos = {g_algoRandom, g_algoAway, g_algoHunter}

g_prevYard = []
g_possibleChickenAlgos = g_allPossibleChickenAlgos.copy()


def hunt(yard):
    global g_prevYard
    global g_possibleChickenAlgos

    if isNewYard(g_prevYard, yard):
        g_prevYard = []
        g_possibleChickenAlgos = g_allPossibleChickenAlgos
    else:
        g_possibleChickenAlgos &= getPossibleChickenAlgos(g_prevYard, yard)

    myLoc = findChar(yard, Misc.s_hobbitSelf)
    otherLoc = findChar(yard, Misc.s_hobbitOther)

    hobALoc = min(myLoc, otherLoc)
    hobBLoc = max(myLoc, otherLoc)

    chickenLoc = findChar(yard, Misc.s_chicken)
    awayChickenLocs = getNextChickenLocs(yard, max)
    awayDists = [findDistsFromLoc(yard, loc) for loc in awayChickenLocs]
    #TODO: move towards where chicken will be, not where it is

    dists = findDistsFromLoc(yard, chickenLoc)

    hobANextClosestLocs = nextClosestLocs(dists, hobALoc)
    hobBNextClosestLocs = nextClosestLocs(dists, hobBLoc)

    hobANextLoc, hobBNextLoc = min(
        [locPair for locPair in itertools.product(
            hobANextClosestLocs + [hobALoc], hobBNextClosestLocs + [hobBLoc])
            if locPair[0] != locPair[1]],
        key = lambda locPair:
            locPair[0].getVal(dists) + locPair[1].getVal(dists)
    )

    g_prevYard = yard

    if myLoc == hobALoc:
        return Loc.s_principalDels[hobANextLoc - hobALoc]

    return Loc.s_principalDels[hobBNextLoc - hobBLoc]


def isNewYard(prevYard, currYard):
    if not prevYard:
        return True

    if len(prevYard) != len(currYard) or len(prevYard[0]) != len(currYard[0]):
        return True

    for r in range(len(currYard)):
        for c in range(len(currYard[r])):
            if((prevYard[r][c] == Misc.s_wall)
                != (currYard[r][c] == Misc.s_wall)
            ):
                return True

    prevChickenLoc = findChar(prevYard, Misc.s_chicken)
    currChickenLoc = findChar(currYard, Misc.s_chicken)

    if prevChickenLoc.euclidDist(currChickenLoc) >= 2:
        return True

    prevHobSelfLoc = findChar(prevYard, Misc.s_hobbitSelf)
    currHobSelfLoc = findChar(currYard, Misc.s_hobbitSelf)

    prevHobOtherLoc = findChar(prevYard, Misc.s_hobbitOther)
    currHobOtherLoc = findChar(currYard, Misc.s_hobbitOther)

    if prevHobSelfLoc.euclidDist(currHobOtherLoc) >= 2:
        return True

    if currHobSelfLoc.euclidDist(prevHobOtherLoc) >= 2:
        return True

    return False


def makeYardNode(yard):
    chickenLoc = findChar(yard, Misc.s_chicken)
    hobSelfLoc = findChar(yard, Misc.s_hobbitSelf)
    hobOtherLoc = findChar(yard, Misc.s_hobbitOther)

    hobALoc, hobBLoc = sorted([hobALoc, hobBLoc])

    yardNode = YardNode(yard, chickenLoc, hobALoc, hobBLoc)
    return yardNode


def makeYardGraph(startYard):
    yardNodeToHobbitNodes = collections.defaultdict(list)
    yardNodeToExtra = {}

    #TODO: need to branch on hobbit moves, THEN chicken moves

    startNode = makeYardNode(startYard)
    yardNodeQ = collections.deque([startNode])
    yardNodeToExtra[startNode] = YardExtra(stepNum=1, parentNode=None)

    while yardNodeQ:
        yardNode = yardNodeQ.popleft()
        extra = yardNodeToExtra[yardNode]

        nextChickenLocs = getNextActorLocs(yardNode, yardNode.chickenLoc)
        nextHobALocs = getNextActorLocs(yardNode, yardNode.hobALoc)
        nextHobBLocs = getNextActorLocs(yardNode, yardNode.hobBLoc)

        nextHobLocPairs = sorted(set(
            tuple(sorted((nextHobALoc, nextHobBLoc)))
            for nextHobALoc, nextHobBLoc
            in itertools.product(nextHobALocs, nextHobBLocs)
            if nextHobALoc != nextHobBLoc
        ))

        for nextHobALoc, nextHobBLoc in nextHobLocPairs:
            hobbitNode = HobbitNode(nextHobALoc, nextHobBLoc, [])

            for nextChickenLoc in nextChickenLocs:
                if nextChickenLoc in (nextHobALoc, nextHobBLoc):
                    nextChickenLoc = None

                possibleYardNode = makeYardNode(
                    yardNode.yard, nextChickenLoc, nextHobALoc, nextHobBLoc))

                #TODO: gosh, if we already have such a node, then maybe the whole nextHobLocPair should be scrapped?

                hobbitNode.possibleYardNodes.append(possibleYardNode)

                if nextChickenLoc is not None:
                    yardNodeQ.append(possibleYardNode)


'''
def getPossibleChickenAlgos(prevYard, currYard):
    prevHobSelfLoc = findChar(prevYard, Misc.s_hobbitSelf)
    currHobSelfLoc = findChar(currYard, Misc.s_hobbitSelf)

    prevHobOtherLoc = findChar(prevYard, Misc.s_hobbitOther)
    currHobOtherLoc = findChar(currYard, Misc.s_hobbitOther)

    prevChickenLoc = findChar(prevYard, Misc.s_chicken)
    currChickenLoc = findChar(currYard, Misc.s_chicken)

    awayChickenLocs = getNextChickenLocs(prevYard, max)
    hunterChickenLocs = getNextChickenLocs(prevYard, min)

    possibleChickenAlgos = {g_algoRandom}
    possibleChickenNextLocs = []

    if currChickenLoc in awayChickenLocs:
        possibleChickenAlgos.add(g_algoAway)

    if currChickenLoc in hunterChickenLocs:
        possibleChickenAlgos.add(g_algoHunter)

    return possibleChickenAlgos
'''


'''
def getNextChickenLocs(yardNode, distSelector=None):

    potentialNextChickenLocs = yardNode.chickenLoc.principalNeighbors(
        yard, True)

    if distSelector is None:
        return potentialNextChickenLocs

    potentialChickenDists = [
        min(loc.euclidDist(yard.hobALoc), loc.euclidDist(yard.hobBLoc))
        for loc in potentialNextChickenLocs
    ]

    selectedDist = distSelector(potentialChickenDists)

    nextChickenLocs = [
        loc for i, loc in enumerate(potentialNextChickenLocs)
        if potentialChickenDists[i] == selectedDist
    ]

    return nextChickenLocs
'''


def getNextActorLocs(yardNode, actorLoc)
    if actorLoc.getVal(yardNode.yard) == Misc.s_chicken:
        return actorLoc.principalNeighbors(yardNode.yard, True)

    return actorLoc.principalNeighbors(yardNode.yard, False)


def findDistsFromLoc(yard, startLoc):
    dists = [[None] * len(yard[0]) for row in yard]

    startLoc.setVal(dists, 0)
    frontier = collections.deque([startLoc])

    while frontier:
        newlySolvedLoc = frontier.popleft()
        newlySolvedDist = newlySolvedLoc.getVal(dists)

        for neighbor in newlySolvedLoc.principalNeighbors(yard):
            neighborDist = neighbor.getVal(dists)

            if neighborDist is None or newlySolvedDist + 1 < neighborDist:
                neighbor.setVal(dists, newlySolvedDist + 1)
                frontier.append(neighbor)

    return dists


def findChar(yard, symb):
    for r, row in enumerate(yard):
        for c, ch in enumerate(row):
            if ch == symb:
                return Loc(r, c)
    return None, None


def nextClosestLocs(dists, currLoc):
    currDist = currLoc.getVal(dists)
    nextLocs = [
        neighbor for neighbor in currLoc.principalNeighbors(dists)
        if neighbor.getVal(dists) == currDist - 1
    ]

    return nextLocs


if __name__ == "__main__":
    # These checker is using only for your local testing;
    # It's run function in the same environment,
    # but in the grading it will be in various;
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
            if(0 <= nx < len(yard) and 0 <= ny < len(yard[0])
                and yard[nx][ny] == "."
            ):
                result.append((k, (nx, ny)))
        return result

    def prepare_yard(yard, numb):
        return tuple(sub("\d", "S", row.replace(str(numb), "I"))
            for row in yard)

    def checker(func, yard, chicken_algorithm="random"):
        # clear user globals
        g_prevYard = []

        for _ in range(MAX_STEP):
            print("\n".join(yard) + "\n")
            individual_yards = [prepare_yard(yard, i + 1) for i in range(N)]
            results = [func(y) for y in individual_yards]

            if any(not isinstance(r, str) or r not in DIRS.keys()
                for r in results
            ):
                print(ERROR_TYPE)
                return False

            chicken = find_position(yard, "C")
            possibles = find_free(yard, chicken)
            chicken_action, new_chicken = CHICKEN_ALGORITHM[chicken_algorithm](
                yard, possibles)
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
            temp_yard = [
                [ch if ch in ".X" else "." for ch in row]
                for row in yard]

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
        ), "random"), "Prompt Example Random"

    assert checker(hunt, (
        "......",
        ".1.XX.",
        "...CX.",
        ".XX.X.",
        "...2..",
        "......",
        ), "run_away"), "Prompt Example Away"

    assert checker(hunt, (
        "......",
        ".1.XX.",
        "...CX.",
        ".XX.X.",
        "...2..",
        "......",
        ), "hunter"), "Prompt Example Hunter"

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

