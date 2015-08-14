'''
author: Jacob Egner
date: 2015-06-??
island: home

puzzle URLs:
http://www.checkio.org/mission/x-o-referee/
https://github.com/Bryukh-Checkio-Tasks/checkio-task-x-o-referee

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles
'''


def checkio(grid):
    lines = grid # rows
    lines.extend(zip(*grid)) # cols
    lines.append([grid[0][0], grid[1][1], grid[2][2]]) # diag 1
    lines.append([grid[0][2], grid[1][1], grid[2][0]]) # diag 2

    for line in lines:
        for player in ('X', 'O'):
            if all(map(lambda cell: cell == player, line)):
                return player
    return 'D'


if __name__ == '__main__':
    assert checkio([
        "X.O",
        "XX.",
        "XOO"]) == "X", "Xs wins"
    assert checkio([
        "OO.",
        "XOX",
        "XOX"]) == "O", "Os wins"
    assert checkio([
        "OOX",
        "XXO",
        "OXX"]) == "D", "Draw"
    assert checkio([
        "O.X",
        "XX.",
        "XOO"]) == "X", "Xs wins again"

