'''
author: Jacob Egner
date: 2015-07-05
island: mine
http://www.checkio.org/mission/supply-stations/
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-supply-stations
'''


import collections
import copy
import itertools
import functools


gc_open = '.'
gc_wall = 'X'
gc_finish = 'F'


class Loc(collections.namedtuple('Loc', ['r', 'c'])):

    def north(self): return Loc(self.r - 1, self.c)
    def south(self): return Loc(self.r + 1, self.c)
    def west(self): return Loc(self.r, self.c - 1)
    def east(self): return Loc(self.r, self.c + 1)

    def cardinalNeighbors(self):
        return [ self.north(), self.east(), self.south(), self.west(), ]


    def principalNeighbors(self):
        return [Loc(r + delR, c + delC) for delR, delC
            in itertools.product([-1, 0, 1], repeat=2) if delR or delC]


    def manhattanDist(self, other):
        return abs(self.r - other.r) + abs(self.c - other.c)


@functools.total_ordering
class VeryBig:
    def __eq__(self, other): return isinstance(other, VeryBig)
    def __lt__(self, other): return False
    def __add__(self, other): return self
    def __radd__(self, other): return self


class Edge(collections.namedtuple('Edge', ['srcId', 'dstId', 'cost'])):
    pass


@functools.total_ordering
class Node:

    def __init__(self, nodeId, edges, estimatedRemainingDist = 0):
        self.nodeId = nodeId
        self.edges = edges
        self.pathParent = None
        self.currDist = VeryBig()
        self.estimatedRemainingDist = estimatedRemainingDist


    def __str__(self):
        return str(self.nodeId)


    def __repr__(self):
        return "Node(id={},parent={},currDist={},remDist={},edges={})".format(
            self.nodeId,
            self.pathParent,
            self.currDist,
            self.estimatedRemainingDist,
            self.edges);


    def __eq__(self, other):
        return self.possibleTotalPathLen() == other.possibleTotalPathLen()


    def __lt__(self, other):
        return self.possibleTotalPathLen() < other.possibleTotalPathLen()


    def possibleTotalPathLen(self):
        return self.currDist + self.estimatedRemainingDist


    def getNeighborIds(self):
        return [edge.dstId for edge in self.edges]


class AStar:

    def __init__(self, nodeMap, startId, finishId = None):
        '''
        nodeMap is a dict with nodeId keys and Node values;
        finishId being None indicates a desire to calculate shortest dist to
        every node rather than halting once finding a shortest path to a
        particular finish node
        '''
        self.nodeMap = copy.deepcopy(nodeMap)
        self.startId = startId
        self.finishId = finishId
        self.pathToFinish = None


    @staticmethod
    def fromGrid(
        grid,
        startId, finishId,
        neighborIdsAndCostsFunc,
        estimatedRemainingDistFunc
    ):
        nodeMap = {}
        visitedNodeIds = set()
        nodeIdStack = [startId]

        while nodeIdStack:
            nodeId = nodeIdStack.pop()
            estimatedRemainingDist = estimatedRemainingDistFunc(nodeId)
            edges = [Edge(nodeId, neighborId, cost)
                for neighborId, cost in neighborIdsAndCostsFunc(nodeId)]

            nodeMap[nodeId] = Node(nodeId, edges, estimatedRemainingDist)

            visitedNodeIds.add(nodeId)

            for edge in edges:
                if edge.dstId not in visitedNodeIds:
                    nodeIdStack.append(edge.dstId)

        return AStar(nodeMap, startId, finishId)


    def solve(self):
        self._explore()
        self._markPath()


    def _explore(self):
        openNodeIds = set()

        self.nodeMap[self.startId].currDist = 0
        openNodeIds.add(self.startId)

        while openNodeIds:
            newlySolvedNode = min(map(
                lambda nodeId: self.nodeMap[nodeId],
                openNodeIds))

            if newlySolvedNode.nodeId == self.finishId:
                break

            openNodeIds.remove(newlySolvedNode.nodeId)

            for edge in newlySolvedNode.edges:
                newDist = newlySolvedNode.currDist + edge.cost
                neighbor = self.nodeMap[edge.dstId]

                if newDist < neighbor.currDist:
                    neighbor.currDist = newDist
                    neighbor.pathParent = newlySolvedNode
                    openNodeIds.add(neighbor.nodeId)


    def _markPath(self):
        if self.finishId is None:
            return

        currNode = self.nodeMap[self.finishId]
        reversePath = []

        while currNode is not None:
            reversePath.append(currNode)
            currNode = currNode.pathParent

        self.pathToFinish = list(reversed(reversePath))


def supply_routes(grid):
    return "", "", "", ""


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
        "....X....."))
    print(test1[1])
    assert test1[0], "First test"

    test2 = checker(supply_routes, (
        "1...2",
        ".....",
        "..F..",
        ".....",
        "3...4"))
    print(test2[1])
    assert test2[0], "Second test"

    test3 = checker(supply_routes, (
        "..2..",
        ".....",
        "1.F.3",
        ".....",
        "..4.."))
    print(test3[1])
    assert test3[0], "Third test"


