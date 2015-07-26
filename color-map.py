'''
author: Jacob Egner
date: 2015-07-25
island: electronic station

puzzle prompt:
http://www.checkio.org/mission/color-map

puzzle prompt source repo:
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-color-map

my checkio solution repo:
https://github.com/jmegner/CheckioPuzzles

strategy is to first extract mapping of country to set of adjacent countries,
then do depth-first recursive search of possible colorings

'''


import collections


gc_colors = (1, 2, 3, 4)
gc_noColor = 0


class Loc(collections.namedtuple('Loc', ['r', 'c'])):

    def __add__(self, other):
        return Loc(self.r + other.r, self.c + other.c)


    def cardinalNeighbors(self):
        return [self + cardinalDel for cardinalDel in self.s_cardinalDels]


    def inBounds(self, grid):
        return(self.r >=0 and self.c >= 0
            and self.r < len(grid) and self.c < len(grid[self.r])
            )


    def getFrom(self, grid):
        return grid[self.r][self.c]


Loc.s_cardinalDels = collections.OrderedDict([
    (Loc(-1, +0), 'N'),
    (Loc(+0, +1), 'E'),
    (Loc(+1, +0), 'S'),
    (Loc(+0, -1), 'W'),
])


def color_map(grid):
    countryToAdjacent = collections.defaultdict(set)

    for r, row in enumerate(grid):
        for c, countryId in enumerate(row):
            loc = Loc(r, c)

            countryToAdjacent[countryId].update([
                adjLoc.getFrom(grid) for adjLoc in loc.cardinalNeighbors()
                if adjLoc.inBounds(grid)
                and adjLoc.getFrom(grid) != countryId])

    countryToColor = [gc_noColor] * len(countryToAdjacent)

    depthFirstSearch(countryToAdjacent, countryToColor)

    return countryToColor


def depthFirstSearch(countryToAdjacent, countryToColor):
    if gc_noColor not in countryToColor:
        return True

    currCountry = countryToColor.index(0)

    for color in gc_colors:
        colorOkay = True

        for adjCountry in countryToAdjacent[currCountry]:
            if countryToColor[adjCountry] == color:
                colorOkay = False
                break

        if colorOkay:
            countryToColor[currCountry] = color

            if depthFirstSearch(countryToAdjacent, countryToColor):
                return True

            countryToColor[currCountry] = gc_noColor

    return False


if __name__ == '__main__':
    NEIGHS = ((-1, 0), (1, 0), (0, 1), (0, -1))
    COLORS = (1, 2, 3, 4)
    ERROR_NOT_FOUND = "Didn't find a color for the country {}"
    ERROR_WRONG_COLOR = "I don't know about the color {}"

    def checker(func, region):
        user_result = func(region)
        if not isinstance(user_result, (tuple, list)):
            print("The result must be a tuple or a list")
            return False
        country_set = set()
        for i, row in enumerate(region):
            for j, cell in enumerate(row):
                country_set.add(cell)
                neighbours = []
                if j < len(row) - 1:
                    neighbours.append(region[i][j + 1])
                if i < len(region) - 1:
                    neighbours.append(region[i + 1][j])
                try:
                    cell_color = user_result[cell]
                except IndexError:
                    print(ERROR_NOT_FOUND.format(cell))
                    return False
                if cell_color not in COLORS:
                    print(ERROR_WRONG_COLOR.format(cell_color))
                    return False
                for n in neighbours:
                    try:
                        n_color = user_result[n]
                    except IndexError:
                        print(ERROR_NOT_FOUND.format(n))
                        return False
                    if cell != n and cell_color == n_color:
                        print("Same color neighbours.")
                        return False
        if len(country_set) != len(user_result):
            print("Excess colors in the result")
            return False
        return True

    assert checker(color_map, (
        (0, 0, 0),
        (0, 1, 1),
        (0, 0, 2),
    )), "Small"

    assert checker(color_map, (
        (0, 0, 2, 3),
        (0, 1, 2, 3),
        (0, 1, 1, 3),
        (0, 0, 0, 0),
    )), "4X4"

    assert checker(color_map, (
        (1, 1, 1, 2, 1, 1),
        (1, 1, 1, 1, 1, 1),
        (1, 1, 0, 1, 1, 1),
        (1, 0, 0, 0, 1, 1),
        (1, 1, 0, 4, 3, 1),
        (1, 1, 1, 3, 3, 3),
        (1, 1, 1, 1, 3, 5),
    )), "6 pack"

