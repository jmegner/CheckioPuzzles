'''
author: Jacob Egner
date: 2015-06-??
island: home

puzzle URLs:
http://www.checkio.org/mission/find-friends/
https://github.com/Bryukh-Checkio-Tasks/checkio-task-find-friends

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles
'''


def check_connection(friendPairs, drone1, drone2):
    directFriends = {}

    for friendPair in friendPairs:
        friendA, friendB = friendPair.split('-')
        directFriends.setdefault(friendA, set()).add(friendB)
        directFriends.setdefault(friendB, set()).add(friendA)

    return isConnected(directFriends, set(), drone1, drone2)


def isConnected(directFriends, touchedDrones, currDrone, destDrone):
    if currDrone == destDrone:
        return True

    if currDrone in touchedDrones:
        return False

    touchedDrones.add(currDrone)

    for friend in directFriends[currDrone]:
        if isConnected(directFriends, touchedDrones, friend, destDrone):
            return True

    return False


if __name__ == '__main__':
    assert check_connection(
        ("dr101-mr99", "mr99-out00", "dr101-out00", "scout1-scout2",
         "scout3-scout1", "scout1-scout4", "scout4-sscout", "sscout-super"),
        "scout2", "scout3") == True, "Scout Brotherhood"
    assert check_connection(
        ("dr101-mr99", "mr99-out00", "dr101-out00", "scout1-scout2",
         "scout3-scout1", "scout1-scout4", "scout4-sscout", "sscout-super"),
        "super", "scout2") == True, "Super Scout"
    assert check_connection(
        ("dr101-mr99", "mr99-out00", "dr101-out00", "scout1-scout2",
         "scout3-scout1", "scout1-scout4", "scout4-sscout", "sscout-super"),
        "dr101", "sscout") == False, "I don't know any scouts."

