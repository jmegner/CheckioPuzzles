# implemented according to http://en.wikipedia.org/wiki/Suurballe%27s_algorithm
# the graph therefore has two vertices for each cell: a "VIN" and a "VOUT".


# imports

from collections import namedtuple
from copy        import deepcopy
from functools   import reduce


# constants

VIN = 0
VOUT = 1


# point

Point = namedtuple("Point", ["x", "y"])


# node

Node = namedtuple("Node", ["p", "t"])


# edge

Edge = namedtuple("Edge", ["f", "t", "c"])

Edge.translate = lambda self: {
    (-1,  0): "W",
    ( 0, -1): "N",
    ( 1,  0): "E",
    ( 0,  1): "S",
    ( 0,  0): ""
}[(self.t.p.x - self.f.p.x, self.t.p.y - self.f.p.y)]


# graph

class Graph:

    def __init__(self):
        self.vertices = []
        self.edges = []


    def clone(self):
        res = Graph()
        res.vertices = deepcopy(self.vertices)
        res.edges = deepcopy(self.edges)
        return res


    def in_edges(self, v):
        return [e for e in self.edges if e.t == v]


    def out_edges(self, v):
        return [e for e in self.edges if e.f == v]


    def is_edge(self, f, t):
        return any(e.f == f and e.t == t for e in self.edges)


    def add_edge(self, f, t, c):
        assert all(e.f != f or e.t != t for e in self.edges)
        self.edges.append(Edge(f, t, c))


    def del_edge(self, f, t):
        self.edges = list(e for e in self.edges if e.f != f or e.t != t)


    def update_edge(self, f, t, c):
        self.del_edge(f, t)
        self.add_edge(f, t, c)


# data

Data = namedtuple("Data", ["graph", "starts", "facto"])


# helpers

def init(grid):

    """
       creates the graph from the input
       each cell is divided in two nodes, VIN and VOUT
         those two nodes are linked with cost 0
       edges are added for all valid steps
         (from neither the factory nor an obstacle, to neither a starting point
          nor an obstacle)
    """

    g = Graph()
    facto = None
    starts = [None] * 4

    for y, r in enumerate(grid):
        for x, v in enumerate(r):
            point = Point(x, y)

            if v in "1234":
                starts[int(v) - 1] = Node(point, VOUT)

            if v == "F":
                facto = Node(point, VIN)

            if v != "X":
                g.vertices.append(Node(point, VIN))
                g.vertices.append(Node(point, VOUT))
                g.add_edge(Node(point, VIN), Node(point, VOUT), 0)
                g.add_edge(Node(point, VOUT), Node(point, VIN), 0)

            if x > 0:
                p = grid[y][x-1]

                if v not in "XF" and p not in "1234X":
                    g.add_edge(Node(point, VOUT), Node(Point(x-1, y), VIN), 1)

                if p not in "XF" and v not in "1234X":
                    g.add_edge(Node(Point(x-1, y), VOUT), Node(point, VIN), 1)

            if y > 0:
                p = grid[y-1][x]

                if v not in "XF" and p not in "1234X":
                    g.add_edge(Node(point, VOUT), Node(Point(x, y-1), VIN), 1)

                if p not in "XF" and v not in "1234X":
                    g.add_edge(Node(Point(x, y-1), VOUT), Node(point, VIN), 1)

    return Data(g, starts, facto)


def make_tree(graph, start, end):
    """
       creates a costmap of all reachable nodes from node start
       also outputs the shortest path (list of edges) from start to end
       this is simply a simplified and adapted dijkstra
       it might be slow in worst case since curv is not sorted
    """

    seen = {start: (None, 0)}
    curv = [start]

    while curv:
        node, curv = curv[0], curv[1:]
        _, cost = seen[node]

        for e in graph.out_edges(node):
            if e.t not in seen or cost + e.c < seen[e.t][1]:
                seen[e.t] = (node, cost + e.c)
                curv.append(e.t)

    path = []

    while end != start:
        path.append(Edge(seen[end][0], end, 0))
        end = seen[end][0]

    return seen, list(reversed(path))


def transform(graph, tree, path):
    """
       transforms a graph according to Suurballe's algorithm
    """

    result = graph.clone()
    result.edges = [Edge(e.f, e.t, e.c + tree[e.f][1] - tree[e.t][1])
                    if e in tree else e for e in graph.edges]

    for e in path:
        result.del_edge(e.f, e.t)
        result.update_edge(e.t, e.f, 0)

    return result


def merge(paths):
    """
       merges a list of paths (list of list of edges), then removes all
       conflicting paths (edges that appear in both directions)
    """

    g = Graph()

    for path in paths:
        for edge in path:
            if edge.f not in g.vertices:
                g.vertices.append(edge.f)

            if edge.t not in g.vertices:
                g.vertices.append(edge.t)

            g.add_edge(edge.f, edge.t, 1)

    g.edges = [e1 for e1 in g.edges
               if all(e2.f != e1.t or e2.t != e1.f for e2 in g.edges)]

    return g


def path(graph, start, end):
    """
       reconstructs the only path that remains from start to end
    """

    path = []

    while start != end:
        assert len(graph.out_edges(start)) == 1

        edge = graph.out_edges(start)[0]
        path.append(edge.translate())
        start = edge.t

    return "".join(path)


# main

def supply_routes(gm):

    data = init(gm)
    paths = []

    def iteration(graph, start):
        tree, path = make_tree(graph, start, data.facto)
        paths.append(path)
        return transform(graph, tree, path)

    reduce(iteration, data.starts, data.graph)
    result = merge(paths)

    return [path(result, start, data.facto) for start in data.starts]


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


