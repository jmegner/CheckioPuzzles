import collections


class Coord(collections.namedtuple('Rc', ['r', 'c'])):

    def naiveNeighbors(self):        
        return [
            Coord(self.r - 1, self.c),
            Coord(self.r,     self.c + 1),
            Coord(self.r + 1, self.c),
            Coord(self.r,     self.c - 1),
            ]
    

class Island:

    c_maxDist = 1e99
    c_water = 0
    c_land = 1    
    c_waterCost = 1
    c_landCost = 100

    def __init__(self, cells):        

        self.numRows = len(cells) + 1
        self.numCols = len(cells[0])
        
        self.cells = [[self.c_water] * self.numCols]
        self.cells.extend(cells)
        
        self.dists = [ [self.c_maxDist] * self.numCols
            for i in range(self.numRows) ]


    def __str__(self):
        return '\n'.join([''.join(row) for row in self.cells])


    def prettyDists(self):
        prettyGrid = ""

        for r in range(self.numRows):
            for c in range(self.numCols):
                dist = self.dists[r][c]

                if dist == self.c_maxDist:
                    prettyGrid += "    X"
                else:
                    prettyGrid += "{:>5d}".format(dist)

            prettyGrid += "\n"

        return prettyGrid


    def getCell(self, coord):
        return self.cells[coord.r][coord.c]


    def getDist(self, coord):
        return self.dists[coord.r][coord.c]


    def setDist(self, coord, dist):
        self.dists[coord.r][coord.c] = dist


    def minPossibleRemainingDist(self, coord):
        return self.c_waterCost * (self.numRows - 1 - coord.r)


    def getWalkableNeighbors(self, coord):
        return [Coord(neighbor.r, neighbor.c)
                for neighbor in coord.naiveNeighbors()
                if self.inBounds(neighbor)]


    def inBounds(self, coord):
        return (coord.r >= 0 and coord.c >= 0
            and coord.r < self.numRows and coord.c < self.numCols)


    def getMinEstimatedTotalDistCoord(self, coords):
        return min(coords, key = lambda coord
            : self.getDist(coord) + self.minPossibleRemainingDist(coord))


    def walkCost(self, coord):
        if self.getCell(coord) == self.c_water:
            return self.c_waterCost
        return self.c_landCost
        
        
    def solve(self):
        openCoords = set()
        
        self.dists[0][0] = 0
        openCoords.add(Coord(0, 0))        
        
        while openCoords:
            newlySolvedCoord = self.getMinEstimatedTotalDistCoord(openCoords)
            
            if newlySolvedCoord.r == self.numRows - 1:                
                numCanals = self.getDist(newlySolvedCoord) // self.c_landCost                
                return numCanals

            openCoords.remove(newlySolvedCoord)
            
            for neighbor in self.getWalkableNeighbors(newlySolvedCoord):
                newNeighborDist = (self.getDist(newlySolvedCoord)
                    + self.walkCost(neighbor))

                if newNeighborDist < self.getDist(neighbor):
                    self.setDist(neighbor, newNeighborDist)
                    openCoords.add(neighbor)
        
        return None


def checkio(land_map):
    isle = Island(land_map)    
    return isle.solve()
    

#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio([[1, 1, 1, 1, 0, 1, 1],
                    [1, 1, 1, 1, 0, 0, 1],
                    [1, 1, 1, 1, 1, 0, 1],
                    [1, 1, 0, 1, 1, 0, 1],
                    [1, 1, 0, 1, 1, 1, 1],
                    [1, 0, 0, 1, 1, 1, 1],
                    [1, 0, 1, 1, 1, 1, 1]]) == 2, "1st example"
    assert checkio([[0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 0, 1, 0, 1, 1],
                    [1, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 0]]) == 3, "2nd example"
    assert checkio([[1, 1, 1, 1, 1, 0, 1, 1],
                    [1, 0, 1, 1, 1, 0, 1, 1],
                    [1, 0, 1, 0, 1, 0, 1, 0],
                    [1, 0, 1, 1, 1, 0, 1, 1],
                    [0, 0, 1, 1, 0, 0, 0, 0],
                    [1, 0, 1, 1, 1, 1, 1, 1],
                    [1, 0, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 0, 1, 1, 1, 1]]) == 2, "3rd example"