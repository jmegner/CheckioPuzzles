'''
author: Jacob Egner
date: 2015-07-31
island: o'reilly

puzzle URLs:
http://www.checkio.org/mission/disposable-teleports/
https://github.com/Bryukh-Checkio-Tasks/checkio-task-disposable-teleports

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

overview: recursive depth-first-search
'''


import collections


def checkio(edgesStr):
    nodeToAdj = collections.defaultdict(set)

    for edgeStr in edgesStr.split(','):
        nodeToAdj[edgeStr[0]].add(edgeStr[1])
        nodeToAdj[edgeStr[1]].add(edgeStr[0])

    cycle = findExhaustiveCycle(nodeToAdj, '1')
    return cycle


def findExhaustiveCycle(nodeToAdj, pathStr):
    currNode = pathStr[-1]

    if len(set(pathStr)) == len(nodeToAdj) and currNode == '1':
        return pathStr

    adjNodes = nodeToAdj[currNode]

    for adjNode in adjNodes.copy():
        adjNodes.remove(adjNode)
        nodeToAdj[adjNode].remove(currNode)

        cycle = findExhaustiveCycle(nodeToAdj, pathStr + adjNode)

        if cycle:
            return cycle

        adjNodes.add(adjNode)
        nodeToAdj[adjNode].add(currNode)

    return ''


if __name__ == "__main__":
    def check_solution(func, teleports_str):
        route = func(teleports_str)
        teleports_map = [tuple(sorted([int(x), int(y)])) for x, y in teleports_str.split(",")]
        if route[0] != '1' or route[-1] != '1':
            print("The path must start and end at 1")
            return False
        ch_route = route[0]
        for i in range(len(route) - 1):
            teleport = tuple(sorted([int(route[i]), int(route[i + 1])]))
            if not teleport in teleports_map:
                print("No way from {0} to {1}".format(route[i], route[i + 1]))
                return False
            teleports_map.remove(teleport)
            ch_route += route[i + 1]
        for s in range(1, 9):
            if not str(s) in ch_route:
                print("You forgot about {0}".format(s))
                return False
        return True

    assert check_solution(checkio, "12,23,34,45,56,67,78,81"), "First"
    assert check_solution(checkio, "12,28,87,71,13,14,34,35,45,46,63,65"), "Second"
    assert check_solution(checkio, "12,15,16,23,24,28,83,85,86,87,71,74,56"), "Third"
    assert check_solution(checkio, "13,14,23,25,34,35,47,56,58,76,68"), "Fourth"


