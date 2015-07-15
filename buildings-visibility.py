'''
author: Jacob Egner
date: 2015-07-15
island: mine

puzzle prompt:
http://www.checkio.org/mission/buildings-visibility

puzzle prompt source repo:
https://github.com/Bryukh-Checkio-Tasks/checkio-task-buildings-visibility

my checkio solution repo:
https://github.com/jmegner/CheckioPuzzles

'''


import collections
import operator


class WallPiece(collections.namedtuple(
    'WallPieceT',
    ['x1', 'x2', 'z1', 'z2', 'y'])
):
    '''
    a WallPiece is a rectangular section of a building wall;
    x is left-right/west-east, z is up-down, and y is close-far/south-north;
    because we are viewing from the south, we only care about pieces of a
    building's south wall;
    '''

    @staticmethod
    def fromBuildingAttributes(building):
        return WallPiece(
            x1 = building[0],
            x2 = building[2],
            z1 = 0,
            z2 = building[4],
            y = building[1],
        )


    def piecesCreatedByOcclusion(self, other):
        visiblePieceSet = set()

        # if we are in front or there is no occlusion
        if (
            self.y <= other.y
            or self.x1 >= other.x2
            or self.x2 <= other.x1
            or self.z1 >= other.z2
            or self.z2 <= other.z1
        ):
            return None
        # else we are behind and have occlusion
        else:
            visibleInNegXDir = self.x1 < other.x1
            visibleInPosXDir = self.x2 > other.x2
            visibleInNegZDir = self.z1 < other.z1
            visibleInPosZDir = self.z2 > other.z2

            inner = WallPiece(
                x1 = max(self.x1, other.x1),
                x2 = min(self.x2, other.x2),
                z1 = max(self.z1, other.z1),
                z2 = min(self.z2, other.z2),
                y  = self.y,
                )

            # non-corners ......................................................

            if visibleInNegXDir:
                visiblePieceSet.add(WallPiece(
                    x1 = self.x1,
                    x2 = other.x1,
                    z1 = inner.z1,
                    z2 = inner.z2,
                    y = self.y,
                    ))

            if visibleInPosXDir:
                visiblePieceSet.add(WallPiece(
                    x1 = other.x2,
                    x2 = self.x2,
                    z1 = inner.z1,
                    z2 = inner.z2,
                    y = self.y,
                    ))

            if visibleInNegZDir:
                visiblePieceSet.add(WallPiece(
                    x1 = inner.x1,
                    x2 = inner.x2,
                    z1 = self.z1,
                    z2 = other.z1,
                    y = self.y,
                    ))

            if visibleInPosZDir:
                visiblePieceSet.add(WallPiece(
                    x1 = inner.x1,
                    x2 = inner.x2,
                    z1 = other.z2,
                    z2 = self.z2,
                    y = self.y,
                    ))

            # corners ..........................................................

            if visibleInNegXDir and visibleInNegZDir:
                visiblePieceSet.add(WallPiece(
                    x1 = self.x1,
                    x2 = other.x1,
                    z1 = self.z1,
                    z2 = other.z1,
                    y = self.y,
                    ))

            if visibleInNegXDir and visibleInPosZDir:
                visiblePieceSet.add(WallPiece(
                    x1 = self.x1,
                    x2 = other.x1,
                    z1 = other.z2,
                    z2 = self.z2,
                    y = self.y,
                    ))

            if visibleInPosXDir and visibleInNegZDir:
                visiblePieceSet.add(WallPiece(
                    x1 = other.x2,
                    x2 = self.x2,
                    z1 = self.z1,
                    z2 = other.z1,
                    y = self.y,
                    ))

            if visibleInPosXDir and visibleInPosZDir:
                visiblePieceSet.add(WallPiece(
                    x1 = other.x2,
                    x2 = self.x2,
                    z1 = other.z2,
                    z2 = self.z2,
                    y = self.y,
                    ))

        return visiblePieceSet


def checkio(buildings):
    southWalls = []

    for building in buildings:
        southWalls.append(WallPiece.fromBuildingAttributes(building))

    # sort so that we only have to worry about breaking up walls as we add them
    southWalls = sorted(southWalls, key = operator.attrgetter('y'))

    origWallToVisibleWallPieces = {}

    for southWall in southWalls:
        incorporateFarWall(origWallToVisibleWallPieces, southWall)

    return len(origWallToVisibleWallPieces)


def incorporateFarWall(origWallToVisibleWallPieces, farWall):
    farWallPieces = set([farWall])

    for origWall, existingWallPieces in origWallToVisibleWallPieces.items():
        for existingWallPiece in existingWallPieces:
            farWallPiecesToDestroy = set()
            farWallPiecesToAdd = set()

            for farWallPiece in farWallPieces:
                createdWallPieces = farWallPiece.piecesCreatedByOcclusion(
                    existingWallPiece)

                if createdWallPieces is not None:
                    farWallPiecesToDestroy.add(farWallPiece)
                    farWallPiecesToAdd |= createdWallPieces

            farWallPieces -= farWallPiecesToDestroy
            farWallPieces |= farWallPiecesToAdd

    if farWallPieces:
        origWallToVisibleWallPieces[farWall] = farWallPieces


if __name__ == '__main__':
    assert checkio([
        [1, 1, 4, 5, 3.5],
        [2, 6, 4, 8, 5],
        [5, 1, 9, 3, 6],
        [5, 5, 6, 6, 8],
        [7, 4, 10, 6, 4],
        [5, 7, 10, 8, 3],
    ]) == 5, "First"

    assert checkio([
        [1, 1, 11, 2, 2],
        [2, 3, 10, 4, 1],
        [3, 5, 9, 6, 3],
        [4, 7, 8, 8, 2],
    ]) == 2, "Second"

    assert checkio([
        [1, 1, 3, 3, 6],
        [5, 1, 7, 3, 6],
        [9, 1, 11, 3, 6],
        [1, 4, 3, 6, 6],
        [5, 4, 7, 6, 6],
        [9, 4, 11, 6, 6],
        [1, 7, 11, 8, 3.25],
    ]) == 4, "Third"

    assert checkio([
        [0, 0, 1, 1, 10],
    ]) == 1, "Alone"

    assert checkio([
        [2, 2, 3, 3, 4],
        [2, 5, 3, 6, 4],
    ]) == 1, "Shadow"


