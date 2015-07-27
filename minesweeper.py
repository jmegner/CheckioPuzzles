'''
author: Jacob Egner
date: 2015-07-26
island: electronic station

puzzle prompt:
http://www.checkio.org/mission/minesweeper

puzzle prompt source repo:
https://github.com/Bryukh-Checkio-Tasks/checkio-task-minesweeper

my checkio solution repo:
https://github.com/jmegner/CheckioPuzzles

note: this is an incomplete solution.  It would not solve this field: [
    [0, 1, X]
    [0, 2, 2]
    [0, 1, X]
]

'''


import collections
import itertools


class CellType:
    unknown = -1
    mine = 9
    info = list(range(0, 9))
    #safeUnknown = 10


class Loc(collections.namedtuple('Loc', ['r', 'c'])):

    def __add__(self, other):
        return Loc(self.r + other.r, self.c + other.c)


    def inBounds(self, grid):
        return(self.r >=0 and self.c >= 0
            and self.r < len(grid) and self.c < len(grid[self.r])
            )


    def principalNeighbors(self):
        return [Loc(self.r + rDel, self.c + cDel) for rDel, cDel
            in itertools.product(range(-1, 2), repeat = 2)
            if rDel or cDel
            ]


    def getFrom(self, grid):
        return grid[self.r][self.c]


def checkio(grid):
    numR = len(grid)
    numC = len(grid[0])

    for r, c in itertools.product(range(numR), range(numC)):
        currLoc = Loc(r, c)

        revealAction = nextRevealAction(grid, currLoc)

        if revealAction is not None:
            return revealAction

    return [False, 0, 0]


def nextRevealAction(grid, currLoc):
    numAdjMines = currLoc.getFrom(grid)

    if numAdjMines not in CellType.info:
        return None

    numUnfoundMines = numAdjMines
    numAdjUnknown = 0
    adjUnknownLoc = None

    for adjLoc in currLoc.principalNeighbors():
        if not adjLoc.inBounds(grid):
            continue

        cell = adjLoc.getFrom(grid)

        if cell == CellType.mine:
            numUnfoundMines -= 1
        elif cell == CellType.unknown:
            numAdjUnknown += 1
            adjUnknownLoc = adjLoc

    if numAdjUnknown > 0:
        if numUnfoundMines == numAdjUnknown:
            return [True, adjUnknownLoc.r, adjUnknownLoc.c]
        elif numUnfoundMines == 0:
            return [False, adjUnknownLoc.r, adjUnknownLoc.c]

    return None


#This part is using only for self-testing
if __name__ == '__main__':

    def check_is_win_referee(input_map):
        unopened = [1 for x in range(10) for y in range(10)
            if input_map[x][y] == -1]
        return not unopened

    def build_map(input_map, mine_map, row, col):
        opened = [(row, col)]
        while opened:
            i, j = opened.pop(0)
            neighs = [
                (i + x, j + y) for x, y in [
                    (-1, -1), (-1, 0), (-1, 1), (0, -1),
                    (0, 1), (1, -1), (1, 0), (1, 1)]
                if 0 <= i + x < 10 and 0 <= j + y < 10
            ]

            value = sum([mine_map[k][l] for k, l in neighs])
            input_map[i][j] = value
            if not value:
                for k, l in neighs:
                    if input_map[k][l] == -1 and (k, l) not in opened:
                        opened.append((k, l))
        return input_map

    def check_solution(func, mine_map):
        input_map = [[-1] * 10 for _ in range(10)]
        while True:

            is_mine, row, col = func([row[:] for row in input_map])  # using copy
            if input_map[row][col] != -1:
                print("You tried to uncover or mark already opened cell.")
                return False
            if is_mine and not mine_map[row][col]:
                print("You marked the wrong cell.")
                return False
            if not is_mine and mine_map[row][col]:
                print("You uncovered a mine. BANG!")
                return False
            if is_mine:
                input_map[row][col] = 9
            else:
                build_map(input_map, mine_map, row, col)
            if check_is_win_referee(input_map):
                return True
        return False

    assert check_solution(checkio, [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]), "Simple"

    assert check_solution(checkio, [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]), "Gate"

    assert check_solution(checkio, [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0]]), "Various"

