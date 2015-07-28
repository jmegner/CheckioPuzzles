'''
author: Jacob Egner
date: 2015-07-27
island: elementary

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

'''


class Friends:

    def __init__(self, connections):
        self.connections = list(connections)


    def add(self, connection):
        if connection not in self.connections:
            self.connections.append(connection)
            return True

        return False


    def remove(self, connection):
        if connection in self.connections:
            self.connections.remove(connection)
            return True

        return False


    def names(self):
        nameSet = set()

        for connection in self.connections:
            nameSet |= connection

        return nameSet


    def connected(self, name):
        nameSet = set()

        for connection in self.connections:
            if name in connection:
                nameSet |= connection

        nameSet.discard(name)
        return nameSet


if __name__ == '__main__':
    letter_friends = Friends(({"a", "b"}, {"b", "c"}, {"c", "a"}, {"a", "c"}))
    digit_friends = Friends([{"1", "2"}, {"3", "1"}])
    assert letter_friends.add({"c", "d"}) is True, "Add"
    assert letter_friends.add({"c", "d"}) is False, "Add again"
    assert letter_friends.remove({"c", "d"}) is True, "Remove"
    assert digit_friends.remove({"c", "d"}) is False, "Remove non exists"
    assert letter_friends.names() == {"a", "b", "c"}, "Names"
    assert letter_friends.connected("d") == set(), "Non connected name"
    assert letter_friends.connected("a") == {"b", "c"}, "Connected name"


