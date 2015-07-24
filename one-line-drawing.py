'''
author: Jacob Egner
date: 2015-07-24
island: electronic station

puzzle prompt:
http://www.checkio.org/mission/one-line-drawing/

puzzle prompt source repo:
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-one-line-drawing

my checkio solution repo:
https://github.com/jmegner/CheckioPuzzles

My solution uses Fleury's algorithm to construct a Eulerian trail/path
https://en.wikipedia.org/wiki/Eulerian_path#Fleury.27s_algorithm

1: start at a node of odd degree (or arbitrary node if only even degree nodes);

2: if there is an edge at current node that not needed to keep graph connected,
then travel-and-delete along that edge, else travel-and-delete along any edge
at current node

3: when no edges left, the order of edges traveled-and-deleted is the Eulerian
path/trail

note: there's a lot of use of 'sorted' so that the algorithm has behavior that
does not depend on implementation quirks of set iteration order that can vary
between python versions

'''


import collections


class NodeId(collections.namedtuple('NodeId', ['x', 'y'])):

    def __repr__(self):
        return "N({},{})".format(self.x, self.y)


class Edge(collections.namedtuple('Edge', ['src', 'dst'])):

    def __repr__(self):
        return "E({},{})".format(self.src, self.dst)


    def reversed(self):
        return Edge(self.dst, self.src)


def getNodesOfOddDegree(nodeToEdges):
    return [node for node, edges in nodeToEdges.items() if len(edges) % 2 == 1]


def draw(segments):
    nodeToEdges = collections.defaultdict(set)
    numEdges = 0

    for segment in sorted(segments):
        node1 = NodeId(segment[0], segment[1])
        node2 = NodeId(segment[2], segment[3])

        nodeToEdges[node1].add(Edge(node1, node2))
        nodeToEdges[node2].add(Edge(node2, node1))
        numEdges += 1

    oddNodes = getNodesOfOddDegree(nodeToEdges)

    # Euler trail impossible with more than two odd-degree nodes
    if len(oddNodes) > 2:
        return []

    # must start at an odd node if there is one
    if oddNodes:
        eulerTrail = [sorted(oddNodes)[0]]
    # else does not matter which node we start at
    else:
        eulerTrail = [sorted(nodeToEdges.keys())[0]]

    while numEdges:
        travelEdge = getNextTravelEdge(nodeToEdges, eulerTrail[-1])

        nodeToEdges[travelEdge.src].remove(travelEdge)
        nodeToEdges[travelEdge.dst].remove(travelEdge.reversed())
        numEdges -= 1

        eulerTrail.append(travelEdge.dst)

    return eulerTrail


def getNextTravelEdge(nodeToEdges, currNode):
    edges = sorted(nodeToEdges[currNode])

    for edge in edges:
        if not graphHasDecreasedConnectivityWithoutEdge(nodeToEdges, edge):
            return edge

    if edges:
        return next(iter(edges))

    raise ValueError("no remaining edges at node")


def graphHasDecreasedConnectivityWithoutEdge(nodeToEdges, ignoredEdge):

    # quick check for removing last edge of a node
    if(len(nodeToEdges[ignoredEdge.src]) == 1
        or len(nodeToEdges[ignoredEdge.dst]) == 1
    ):
        return True

    # otherwise must see if we can touch all nodes with edges

    nodesWithEdges = sorted([
        node for node, edges in nodeToEdges.items() if edges])

    nodeStack = [nodesWithEdges[0]]
    touchedNodes = set(nodeStack)

    while nodeStack and len(touchedNodes) < len(nodesWithEdges):
        currNode = nodeStack.pop()

        for edge in sorted(nodeToEdges[currNode]):
            if(sorted(edge) != sorted(ignoredEdge)
                and edge.dst not in touchedNodes
            ):
                nodeStack.append(edge.dst)
                touchedNodes.add(edge.dst)

    return len(touchedNodes) < len(nodesWithEdges)


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for
    # auto-testing
    def checker(func, in_data, is_possible=True):
        user_result = func(in_data)
        if not is_possible:
            if user_result:
                print("How did you draw this?")
                return False
            else:
                return True
        if len(user_result) < 2:
            print("More points please.")
            return False
        data = list(in_data)
        for i in range(len(user_result) - 1):
            f, s = user_result[i], user_result[i + 1]
            if (f + s) in data:
                data.remove(f + s)
            elif (s + f) in data:
                data.remove(s + f)
            else:
                print("The wrong segment {}.".format(f + s))
                return False
        if data:
            print("You forgot about {}.".format(data[0]))
            return False
        return True

    assert checker(draw,
        {
            (1, 2, 1, 5),
            (1, 2, 7, 2),
            (1, 5, 4, 7),
            (4, 7, 7, 5),
        }, True), "Example 1"

    assert checker(draw,
        {
            (1, 2, 1, 5),
            (1, 2, 7, 2),
            (1, 5, 4, 7),
            (4, 7, 7, 5),
            (7, 5, 7, 2),
            (1, 5, 7, 2),
            (7, 5, 1, 2),
        }, False), "Example 2"

    assert checker(draw,
        {
            (1, 2, 1, 5),
            (1, 2, 7, 2),
            (1, 5, 4, 7),
            (4, 7, 7, 5),
            (7, 5, 7, 2),
            (1, 5, 7, 2),
            (7, 5, 1, 2),
            (1, 5, 7, 5),
        }, True), "Example 3"

    assert checker(draw,
        {
            (1, 1, 1, 9),
            (9, 9, 1, 9),
            (9, 9, 9, 1),
            (9, 1, 1, 1),
        }, True), "square"

    assert checker(draw,
        {
            (1, 1, 2, 2),
            (2, 1, 2, 2),
            (2, 1, 3, 2),
            (2, 1, 3, 1),
            (1, 1, 0, 2),
            (1, 1, 0, 0),
            (3, 2, 3, 1),
            (0, 0, 0, 2)
        }, True), "extra 6"

    assert checker(draw,
        {
            (1, 1, 2, 2),
            (3, 3, 2, 2),
            (3, 3, 4, 4),
            (3, 3, 5, 5),
            (1, 1, 6, 6),
            (1, 1, 7, 7),
            (4, 4, 5, 5),
            (7, 7, 6, 6)
        }, True), "extra 6, shuffle1"

    assert checker(draw,
        {
            (4,2,6,8),
            (2,4,6,2),
            (4,8,6,2),
            (2,4,6,8),
            (6,8,6,2),
            (6,2,8,4),
            (4,2,8,4),
            (2,6,4,8),
            (2,6,6,8),
            (2,6,4,2),
            (4,2,4,8),
            (2,4,4,8),
            (4,8,6,8),
            (2,4,4,2),
            (2,4,8,4),
            (6,8,8,4),
            (2,6,6,2),
            (2,6,8,4),
            (4,2,6,2),
            (4,8,8,4),
            (2,4,2,6),
        }, True), "edge 4"


