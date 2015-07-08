'''
author: Jacob Egner
date: 2015-07-05
island: mine

puzzle prompt:
http://www.checkio.org/mission/supply-stations/

puzzle prompt source repo:
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-supply-stations

my checkio solution repo:
https://github.com/jmegner/CheckioPuzzles

'''


import collections
import copy
import itertools
import functools


gc_open = '.'
gc_wall = 'X'
gc_finish = 'F'
gc_starts = ['1', '2', '3', '4']
gc_continues = ['a', 'b', 'c', 'd']
gc_walkables = [gc_open, gc_finish]


class Loc(collections.namedtuple('Loc', ['r', 'c'])):

    def north(self): return Loc(self.r - 1, self.c)
    def south(self): return Loc(self.r + 1, self.c)
    def west(self): return Loc(self.r, self.c - 1)
    def east(self): return Loc(self.r, self.c + 1)

    def cardinalNeighbors(self):
        return [ self.north(), self.east(), self.south(), self.west(), ]


    def manhattanDist(self, other):
        return abs(self.r - other.r) + abs(self.c - other.c)


    def __sub__(self, other):
        return Loc(self.r - other.r, self.c - other.c)


@functools.total_ordering
class VeryBig:
    def __eq__(self, other): return isinstance(other, VeryBig)
    def __lt__(self, other): return False
    def __add__(self, other): return self
    def __radd__(self, other): return self


class Multimaze:

    def __init__(self, cells):
        self.cells = [list(row) for row in cells]

        self.numRows = len(cells)
        self.numCols = len(cells[0])
        self.numStations = len(gc_starts)

        self.finishLoc = self.getLocOfCellType(gc_finish)
        self.paths = None
        self.pathStrs = None


    def __str__(self):
        return '\n'.join([''.join(row) for row in self.cells])


    def getCell(self, loc):
        return self.cells[loc.r][loc.c]


    def setCell(self, loc, value):
        self.cells[loc.r][loc.c] = value


    def inBounds(self, loc):
        return (loc.r >= 0 and loc.c >= 0
            and loc.r < self.numRows and loc.c < self.numCols)


    def isWalkable(self, loc):
        return self.inBounds(loc) and self.getCell(loc) in gc_walkables


    def getWalkableNeighbors(self, loc):
        return [neighbor for neighbor in loc.cardinalNeighbors()
                if self.isWalkable(neighbor)]


    def getNextLocs(self, currLoc):
        return [nextLoc for nextLoc in currLoc.cardinalNeighbors()
            if self.isWalkable(nextLoc)
            and self.getNumNeighborsOfType(nextLoc, self.getCell(currLoc)) <= 1
            ]

    def getNumNeighborsOfType(self, loc, cellType):
        return sum([self.getCell(adjLoc) == cellType
            for adjLoc in loc.cardinalNeighbors()
            if self.inBounds(adjLoc)])


    def getLocOfCellType(self, cellType):
        for r in range(self.numRows):
            for c in range(self.numCols):
                if self.cells[r][c] == cellType:
                    return Loc(r, c)
        return None


    def getSortedByFinishProximity(self, locs):
        return sorted(locs, key = lambda loc: loc.manhattanDist(self.finishLoc))


    def solve(self):
        self.paths = [[self.getLocOfCellType(startChar)]
            for startChar in gc_starts]

        self.pathStrs = []

        success = self.depthFirstSearch(0)

        if success:
            delLocToDir = {
                Loc(-1, 0) : 'N',
                Loc(+1, 0) : 'S',
                Loc(0, -1) : 'W',
                Loc(0, +1) : 'E',
                }

            for path in self.paths:
                pathDirs = []

                for currLoc, prevLoc in zip(path[1:], path[:-1]):
                    delLoc = currLoc - prevLoc
                    pathDirs.append(delLocToDir[delLoc])

                self.pathStrs.append(''.join(pathDirs))


    def isSolved(self):
        return all(map(lambda path: path[-1] == self.finishLoc), self.paths)


    def pathReachesFinish(self, path):
        return path[-1] == self.finishLoc


    def depthFirstSearch(self, pathIdx):
        if pathIdx >= len(self.paths):
            return True

        if not self.allStationsCanReachFinish():
            return False

        path = self.paths[pathIdx]
        nextLocs = self.getNextLocs(path[-1])

        if self.finishLoc in nextLocs:
            path.append(self.finishLoc)
            laterSuccess = self.depthFirstSearch(pathIdx + 1)

            if laterSuccess:
                return True

            path.pop()

        else:
            for nextLoc in self.getSortedByFinishProximity(nextLocs):
                path.append(nextLoc)
                self.setCell(nextLoc, gc_continues[pathIdx])

                laterSuccess = self.depthFirstSearch(pathIdx)

                if laterSuccess:
                    return True

                path.pop()
                self.setCell(nextLoc, gc_open)

        return False


    def allStationsCanReachFinish(self):
        for path in self.paths:
            if not self.pathExistsToFinish(path[-1]):
                return False

        return True


    def pathExistsToFinish(self, startLoc):
        if startLoc == self.finishLoc:
            return True

        locStack = [startLoc]
        visitedLocs = set()

        while locStack:
            currLoc = locStack.pop()
            visitedLocs.add(currLoc)

            for adjLoc in self.getWalkableNeighbors(currLoc):
                if adjLoc not in visitedLocs:
                    if adjLoc == self.finishLoc:
                        return True
                    locStack.append(adjLoc)

        return False


def supply_routes(grid):
    maze = Multimaze(grid)
    maze.solve()
    return maze.pathStrs


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for
    # auto-testing
    DIRS = {
        "N": (-1, 0),
        "S": (1, 0),
        "W": (0, -1),
        "E": (0, 1),
    }

    def checker(f, the_map):
        result = f(the_map)
        if (not isinstance(result, (tuple, list)) and len(the_map) != 4 and
                any(not isinstance(r, str) for r in the_map)):
            return False, "The result must be a list/tuple of four strings"
        stations = [None] * 4
        factory_supply = [0] * 4
        for i, row in enumerate(the_map):
            for j, ch in enumerate(row):
                if ch in "1234":
                    stations[int(ch) - 1] = (i, j)
        wmap = [list(row) for row in the_map]
        width = len(wmap[0])
        height = len(wmap)
        for numb, route in enumerate(result, 1):
            coor = stations[numb - 1]
            for i, ch in enumerate(route):
                if ch not in DIRS.keys():
                    return False, "Routes must contain only NSWE"
                row, col = coor[0] + DIRS[ch][0], coor[1] + DIRS[ch][1]
                if not (0 <= row < height and 0 <= col < width):
                    return False, "Ooops, we lost the route from station {}".format(numb)
                checked = wmap[row][col]
                if checked == "X":
                    return False, "The route {} was struck {} {}".format(numb, coor, (row, col))
                if checked == "F":
                    factory_supply[numb - 1] = 1
                    if i >= len(route):
                        return False, "A route should be ended in the factory"
                    break
                if checked != ".":
                    return False, "Don't intersect routes"
                wmap[row][col] = str(numb)
                coor = row, col
        if factory_supply != [1, 1, 1, 1]:
            return False, "You should deliver all four resources"
        return True, "Great!"

    test1 = checker(supply_routes, (
        "..........",
        ".1X.......",
        ".2X.X.....",
        ".XXX......",
        ".X..F.....",
        ".X........",
        ".X..X.....",
        ".X..X.....",
        "..3.X...4.",
        "....X.....",
        ))
    print(test1[1], "\n")
    assert test1[0], "First test"

    test2 = checker(supply_routes, (
        "1...2",
        ".....",
        "..F..",
        ".....",
        "3...4",
        ))
    print(test2[1], "\n")
    assert test2[0], "Second test"

    test3 = checker(supply_routes, (
        "..2..",
        ".....",
        "1.F.3",
        ".....",
        "..4..",
        ))
    print(test3[1], "\n")
    assert test3[0], "test3"

    test4 = checker(supply_routes, (
        ".....",
        "...X.",
        "3F..1",
        ".4.2.",
        ".....",
        ))
    print(test4[1], "\n")
    assert test4[0], "test4"

    test5 = checker(supply_routes, (
        ".....4...",
        "....3F...",
        ".........",
        "XXXXXXX..",
        "X.....X..",
        "1........",
        "2..X.....",
        ))
    print(test5[1], "\n")
    assert test5[0], "test5"

    test6 = checker(supply_routes, (
        "..........",
        ".F..XXXXX.",
        "..........",
        ".X........",
        ".X........",
        ".X........",
        ".X........",
        ".X......4.",
        ".X.....3X2",
        "........1.",
        ))
    print(test6[1], "\n")
    assert test6[0], "test6"

    test7 = checker(supply_routes, (
        "..........",
        "1.......X.",
        "........X.",
        "........X.",
        "........X.",
        "........X.",
        "34.2....X.",
        "X.........",
        "...X...F.X",
        "....X.....",
        ))
    print(test7[1], "\n")
    assert test7[0], "test7"

    test8 = checker(supply_routes, (
        ".....XX..2",
        ".........3",
        "..X......X",
        "..XXXXXXXX",
        "..........",
        "..........",
        "XXXXXXX...",
        "1.......F4",
        "X.XXXXXX..",
        "..........",
        ))
    print(test8[1], "\n")
    assert test8[0], "test8"


