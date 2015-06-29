def checkio(grid):
    lines = grid # rows
    lines.extend(zip(*grid)) # cols
    lines.append([grid[0][0], grid[1][1], grid[2][2]]) #diag1
    lines.append([grid[0][2], grid[1][1], grid[2][0]]) # diag 2

    for line in lines:
        for player in ('X', 'O'):
            if all(map(lambda cell: cell == player, line)):
                return player
    return 'D'


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
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

