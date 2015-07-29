'''
author: Jacob Egner
date: unknown
island: unknown

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


import collections


class Loc(collections.namedtuple('Loc', ['r', 'c'])):

    def inBounds(self, grid):
        return ( self.r >= 0 and self.c >= 0
            and self.r < len(grid)
            and self.c < len(grid[self.r]) )


def can_pass(matrix, startRc, endRc):
    locStack = [Loc(*startRc)]
    visitedLocs = set()

    while locStack:
        loc = locStack.pop()

        if loc == endRc:
            return True

        visitedLocs.add(loc)

        rcDels = [ [0, -1], [0, +1], [-1, 0], [+1, 0], ]

        for rDel, cDel in rcDels:
            nextLoc = Loc(loc.r + rDel, loc.c + cDel)

            if ( nextLoc.inBounds(matrix) and nextLoc not in visitedLocs
                    and matrix[loc.r][loc.c] == matrix[nextLoc.r][nextLoc.c] ):
                locStack.append(nextLoc)

    return False


if __name__ == '__main__':
    assert can_pass( ((0, 0), (0, 0)), (0, 0), (1, 1) ) == True, "very small"
    assert can_pass(((0, 0, 0, 0, 0, 0),
                     (0, 2, 2, 2, 3, 2),
                     (0, 2, 0, 0, 0, 2),
                     (0, 2, 0, 2, 0, 2),
                     (0, 2, 2, 2, 0, 2),
                     (0, 0, 0, 0, 0, 2),
                     (2, 2, 2, 2, 2, 2),),
                    (3, 2), (0, 5)) == True, 'First example'
    assert can_pass(((0, 0, 0, 0, 0, 0),
                     (0, 2, 2, 2, 3, 2),
                     (0, 2, 0, 0, 0, 2),
                     (0, 2, 0, 2, 0, 2),
                     (0, 2, 2, 2, 0, 2),
                     (0, 0, 0, 0, 0, 2),
                     (2, 2, 2, 2, 2, 2),),
                    (3, 3), (6, 0)) == False, 'First example'


