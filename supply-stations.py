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

overview: Suurballe's algorithm

'''


import collections
import copy
import itertools
import functools


class CellType:
    openSpace = '.'
    wall = 'X'
    finish = 'F'
    starts = ['1', '2', '3', '4']
    continues = ['a', 'b', 'c', 'd']
    walkables = [CellType.openSpace, CellType.finish]


@functools.total_ordering
class VeryBig:
    def __eq__(self, other): return isinstance(other, VeryBig)
    def __lt__(self, other): return False
    def __add__(self, other): return self
    __radd__ = __add__
    __sub__  = __add__
    __rsub__ = __add__


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


class StationGraph:

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


    def findShortestPathToFinish(self):
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


class Loc(collections.namedtuple('Loc', ['r', 'c'])):

    def cardinalNeighbors(self):
        return [self + cardinalDel for cardinalDel in self.s_cardinalDels]


    def manhattanDist(self, other):
        return abs(self.r - other.r) + abs(self.c - other.c)


    def __add__(self, other):
        return Loc(self.r + other.r, self.c + other.c)


    def __sub__(self, other):
        return Loc(self.r - other.r, self.c - other.c)


    def __mul__(self, scaler):
        return Loc(self.r * scaler, self.c * scaler)

    __rmul__ = __mul__


Loc.s_cardinalDels = collections.OrderedDict([
    (Loc(-1, +0), 'N'),
    (Loc(+0, +1), 'E'),
    (Loc(+1, +0), 'S'),
    (Loc(+0, -1), 'W'),
])


class NodeType:
    inbound = 0
    outbound = 1


class DoubleNodeId(collections.namedtuple('DoubleNodeId', ['loc', 'nodeType'])):
    pass


class StationGrid:

    def __init__(self, cells):
        self.cells = [list(row) for row in cells]

        self.numRows = len(cells)
        self.numCols = len(cells[0])
        self.numStations = len(CellType.starts)

        self.finishLoc = self.getLocOfCellType(CellType.finish)
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
        return self.inBounds(loc) and self.getCell(loc) in CellType.walkables


    def getWalkableNeighbors(self, loc):
        return [neighbor for neighbor in loc.cardinalNeighbors()
                if self.isWalkable(neighbor)]


    def getNextLocs(self, currLoc):
        return [nextLoc for nextLoc in currLoc.cardinalNeighbors()
            if self.isWalkable(nextLoc)]

    def getLocOfCellType(self, cellType):
        for r in range(self.numRows):
            for c in range(self.numCols):
                if self.cells[r][c] == cellType:
                    return Loc(r, c)
        return None


    def getSortedByFinishProximity(self, locs):
        return sorted(locs, key = lambda loc: loc.manhattanDist(self.finishLoc))


    def estimatedRemainingDist(self, loc):
        return loc.manhattanDist(self.finishLoc)


    def makeDoubleNodeGraph(self):
        stationLocs = [self.getLocOfCellType(startChar)
            for startChar in CellType.starts]

        fakeStartId = Loc(VeryBig(), VeryBig())
        fakeStartNode = Node(
            fakeStartId,
            [Edge(
                fakeStartId,
                DoubleNodeId(stationLoc, NodeType.inbound),
                0)
                for stationLoc in stationLocs])

        nodeMap = {fakeStartId: fakeStartNode}
        visitedLocs = set()
        locStack = list(stationLocs)

        while locStack:
            currLoc = locStack.pop()
            estRemDist = estimatedRemainingDistFunc(currLoc)
            currInNodeId = DoubleNodeId(currLoc, NodeType.inbound)
            currOutNodeId = DoubleNodeId(currLoc, NodeType.outbound)

            transferEdge = Edge(currInNodeId, currOutNodeId, 0)
            outEdges = [
                Edge(
                    currOutNodeId,
                    DoubleNodeId(neighborLoc, NodeType.inbound),
                    1)
                for neighborLoc in self.getWalkableNeighbors(currLoc)
            ]

            nodeMap[currInNodeId] = Node(currInNodeId, transferEdge, estRemDist)
            nodeMap[currOutNodeId] = Node(currOutNodeId, outEdges, estRemDist)

            visitedLocs.add(currLoc)

            for edge in outEdges:
                if edge.dstId not in visitedLocs:
                    locStack.append(edge.dstId.loc)

        self.stationGraph = StationGraph(
            nodeMap,
            fakeStartId,
            DoubleNodeId(self.finishLoc, NodeType.inbound))


    def solve(self):
        for stationIdx in range(len(CellType.starts)):
            self.stationGraph.findShortestPathToFinish()

        self.paths = [[self.getLocOfCellType(startChar)]
            for startChar in CellType.starts]

        self.pathStrs = []

        success = self.depthFirstSearch(0)

        if success:
            for path in self.paths:
                pathDirs = []

                for currLoc, prevLoc in zip(path[1:], path[:-1]):
                    delLoc = currLoc - prevLoc
                    pathDirs.append(Loc.s_cardinalDels[delLoc])

                self.pathStrs.append(''.join(pathDirs))


    def isSolved(self):
        return all(map(lambda path: path[-1] == self.finishLoc), self.paths)


    def pathReachesFinish(self, path):
        return path[-1] == self.finishLoc


def supply_routes(grid):
    stationGrid = StationGrid(grid)
    stationGrid.solve()
    return stationGrid.pathStrs


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

    testGrids = [
        (
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
        ), (
            "1...2",
            ".....",
            "..F..",
            ".....",
            "3...4",
        ), (
            "..2..",
            ".....",
            "1.F.3",
            ".....",
            "..4..",
        ), (
            "..2..",
            ".....",
            "1.F.3",
            ".....",
            "..4..",
        ), (
            ".....",
            "...X.",
            "3F..1",
            ".4.2.",
            ".....",
        ), (
            ".....4...",
            "....3F...",
            ".........",
            "XXXXXXX..",
            "X.....X..",
            "1........",
            "2..X.....",
        ), (
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
        ), (
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
        ), (
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
        )]

    for testIdx, testGrid in enumerate(testGrids):
        testResult, testMsg = checker(supply_routes, testGrid)
        print(testMsg, "\n")
        assert testResult, "test" + str(testIdx)


