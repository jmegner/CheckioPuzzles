'''
author: Jacob Egner
date: 2015-07-31
island: ice base

puzzle URLs:
http://www.checkio.org/mission/network-loops/
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-network-loops

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

note: some use of sorted to get behavior repeatable

'''


import collections


def find_cycle(connections):
    nodeToAdj = collections.defaultdict(set)

    for node1, node2 in connections:
        nodeToAdj[node1].add(node2)
        nodeToAdj[node2].add(node1)

    longestCycle = findLongestCycle(nodeToAdj, [])
    return longestCycle


def findLongestCycle(nodeToAdj, path):
    if len(path) > 1 and path[0] == path[-1]:
        if len(path) > 3:
            return path
        else:
            return []

    if path:
        nextNodes = sorted(nodeToAdj[path[-1]])
    else:
        nextNodes = sorted(nodeToAdj)

    longestCycle = []

    for nextNode in nextNodes:
        if nextNode not in path or path[0] == nextNode:
            cycle = findLongestCycle(nodeToAdj, path + [nextNode])
            longestCycle = max(longestCycle, cycle, key=len)

    return longestCycle


if __name__ == '__main__':
    def checker(function, connections, best_size):
        user_result = function(connections)
        if not isinstance(user_result, (tuple, list)) or not all(isinstance(n, int) for n in user_result):
            print("You should return a list/tuple of integers.")
            return False
        if not best_size and user_result:
            print("Where did you find a cycle here?")
            return False
        if not best_size and not user_result:
            return True
        if len(user_result) < best_size + 1:
            print("You can find a better loop.")
            return False
        if user_result[0] != user_result[-1]:
            print("A cycle starts and ends in the same node.")
            return False
        if len(set(user_result)) != len(user_result) - 1:
            print("Repeat! Yellow card!")
            return False
        for n1, n2 in zip(user_result[:-1], user_result[1:]):
            if (n1, n2) not in connections and (n2, n1) not in connections:
                print("{}-{} is not exist".format(n1, n2))
                return False
        return True, "Ok"

    assert checker(
        find_cycle,
        (
            (1, 2), (2, 3), (3, 4), (4, 5), (5, 7), (7, 6),
            (8, 5), (8, 4), (1, 5), (2, 4), (1, 8),
        ),
        6), "Example"

    assert checker(
        find_cycle,
        (
            (1, 2), (2, 3), (3, 4), (4, 5), (5, 7), (7, 6), (8, 4), (1, 5), (2, 4),
        ),
        5), "Second"

    assert checker(
        find_cycle,
        ( (3, 4), (2, 3), (1, 2), ),
        0), "Second"


