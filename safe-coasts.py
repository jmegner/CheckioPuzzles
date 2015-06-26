import itertools


INFECT_START = 'I'
DANGEROUS = 'D'
SAFE = 'S'
LAND = 'X'
WATER = '.'

#Loc = collections.namedtuple('Loc', ['r', 'c'])


def finish_map(origGrid):
    grid = [list(row.replace(WATER, SAFE)) for row in origGrid]

    for r, row in enumerate(origGrid):
        for c, origCell in enumerate(row):
            if origCell == DANGEROUS:
                grid[r][c] = INFECT_START
                infectAsDangerous(grid, r, c)

    return [''.join(row) for row in grid]


def infectAsDangerous(grid, r, c):
    def inBounds(r2, c2):
        return r2 >=0 and c2 >= 0 and r2 < len(grid) and c2 < len(grid[0])

    # no need to proceed if we are out of bounds or cell type is dead end
    if not inBounds(r, c) or grid[r][c] == DANGEROUS or grid[r][c] == LAND:
        return

    neighborCoords = list(itertools.product(
        range(r - 1, r + 2), range(c - 1, c + 2)))

    nearLandCoords = [rc for rc in neighborCoords
        if inBounds(*rc) and grid[rc[0]][rc[1]] == LAND]

    # can not declare dangerous if near land
    if nearLandCoords:
        return

    grid[r][c] = DANGEROUS

    rDels = [-1, +1,  0,  0]
    cDels = [ 0,  0, -1, +1]

    # recurse to possibly infect 4 cardinal neighbors
    for rcDel in zip(rDels, cDels):
        infectAsDangerous(grid, r + rcDel[0], c + rcDel[1])


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert isinstance(
        finish_map(("D..", "...", "...")), (list, tuple)), "List or tuple"
    assert list(finish_map((
        "D..XX.....",
        "...X......",
        ".......X..",
        ".......X..",
        "...X...X..",
        "...XXXXX..",
        "X.........",
        "..X.......",
        "..........",
        "D...X....D"))) == [
        "DDSXXSDDDD",
        "DDSXSSSSSD",
        "DDSSSSSXSD",
        "DDSSSSSXSD",
        "DDSXSSSXSD",
        "SSSXXXXXSD",
        "XSSSSSSSSD",
        "SSXSDDDDDD",
        "DSSSSSDDDD",
        "DDDSXSDDDD"], "Example"
    assert list(finish_map((
        "........",
        "........",
        "X.X..X.X",
        "........",
        "...D....",
        "........",
        "X.X..X.X",
        "........",
        "........",))) == [
        "SSSSSSSS",
        "SSSSSSSS",
        "XSXSSXSX",
        "SSSSSSSS",
        "DDDDDDDD",
        "SSSSSSSS",
        'XSXSSXSX',
        "SSSSSSSS",
        "SSSSSSSS"], "Walls"

