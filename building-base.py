'''
author: Jacob Egner
date: 2015-07-24
island: elementary

puzzle prompt:
http://www.checkio.org/mission/building-base

puzzle prompt source repo:
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-building-base

my checkio solution repo:
https://github.com/jmegner/CheckioPuzzles

'''


class Building:

    def __init__(self, south, west, widthWe, widthNs, height=10):
        self.south = south
        self.west = west
        self.widthWe = widthWe
        self.widthNs = widthNs
        self.height = height


    def corners(self):
        north = self.south + self.widthNs
        east = self.west + self.widthWe
        return {
            "south-west" : [self.south, self.west],
            "south-east" : [self.south, east],
            "north-west" : [north, self.west],
            "north-east" : [north, east],
        }


    def area(self):
        return self.widthWe * self.widthNs


    def volume(self):
        return self.area() * self.height


    def __repr__(self):
        return "Building({}, {}, {}, {}, {})".format(
            self.south,
            self.west,
            self.widthWe,
            self.widthNs,
            self.height,
            )


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    def json_dict(d):
        return dict((k, list(v)) for k, v in d.items())

    b = Building(1, 2, 2, 3)
    b2 = Building(1, 2, 2, 3, 5)
    assert json_dict(b.corners()) == {'north-east': [4, 4], 'south-east': [1, 4],
                                      'south-west': [1, 2], 'north-west': [4, 2]}, "Corners"
    assert b.area() == 6, "Area"
    assert b.volume() == 60, "Volume"
    assert b2.volume() == 30, "Volume2"
    assert str(b) == "Building(1, 2, 2, 3, 10)", "String"
