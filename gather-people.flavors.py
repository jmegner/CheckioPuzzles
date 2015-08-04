'''
author: Jacob Egner
date: 2015-08-04
island: ice base

puzzle URLs:
http://www.checkio.org/mission/gather-people/
https://github.com/Bryukh-Checkio-Tasks/checkio-mission-gather-power

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles

These are some various versions I had trying to optimize my score for this
golf style puzzle.
'''


# 128 points, flavor E
def golf(g,t,r=0,v=[]):
    h=g[r]
    e=h[r]
    h[r]=0
    for c,d in enumerate(h):
        if(c not in v)*d*(t-d+1)>0:
            e+=golf(g,t-d,c,v+[c])
    return e


# flavor E, commented and renamed version
# strategy is to do depth-first recursive search outward and see
# what rooms we can reach within the time limit; function returns how many
# people can be evacuated within time limit
def golf(roomGrid, timeRemaining, currRoomIdx=0, visitedRooms=[]):
    roomInfo = roomGrid[currRoomIdx]

    # if we get here within time, that means people in this room can evacuate
    # in time
    numEvacuated = roomInfo[currRoomIdx]

    # do not want to double-count rooms when we re-visit in different recursion
    # branch with more time remaining, so we "evacuate" the people now
    roomInfo[currRoomIdx] = 0

    # look at all possible next rooms to go to
    for nextRoomIdx, timeCost in enumerate(gridRow):
        # go to next room if...
        # 1: have not visited room in this recursion branch
        # 2: next room is connected (signalled by nonzero timeCost)
        # 3: will have non-negative time remaining once in room
        # funky math was done to reduce character count
        if(
            (nextRoomIdx not in visitedRooms)
            * timeCost
            * (timeRemaining - timeCost + 1)
            > 0
        ):
            # fold in evacuated people further down the recursion
            numEvacuated += golf(roomGrid, timeRemaining - timeCost, nextRoomIdx, visitedRooms + [nextRoomIdx])

    return numEvacuated


# 125 points, flavor F
def golf(g,t,r=0,v=[]):
    h=g[r]
    e=h[r]
    h[r]=0
    for c,d in enumerate(h):
        e+=(c not in v)*d*(t-d+1)>0 and golf(g,t-d,c,v+[c])
    return e

# 125 points, flavor C
def golf(g,t,r=0,v=[]):
    h=g[r]
    e=h[r]
    h[r]=0
    for c,d in enumerate(h):
        if d*(t-d+1)>0 and c not in v:
            e+=golf(g,t-d,c,v+[c])
    return e

# 124 points, flavor D
def golf(g,t,r=0,v=[]):
    h=g[r]
    e=h[r]
    h[r]=0
    return e+sum(golf(g,t-d,c,v+[c])for c,d in enumerate(h)if d*(t-d+1)>0 and c not in v)

# 123 points, flavor B
def golf(g,t,r=0):
    h=g[r]
    e=h[r]
    if e<0:return 0
    h[r]=0
    for c,d in enumerate(h):
        if d*(t-d+1)>0:
            h[r]=-1
            e+=golf(g,t-d,c)
            h[r]=0
    return e

# 123 points, flavor A
def golf(g,t,r=0):
    h=g[r]
    e=h[r]
    h[r]=0
    for c,d in enumerate(h):
        if d*(t-d+1)>0:
            h[c]=g[c][r]=0
            e+=golf(g,t-d,c)
            h[c]=g[c][r]=d
    return e

def golf(g,t,r=0):
    h=g[r]
    e=h[r]
    h[r]=0
    for c,d in enumerate(h):
        if d and t-d>=0:
            h[c]=g[c][r]=0
            e+=golf(g,t-d,c)
            h[c]=g[c][r]=d
    return e


# thought I'd see if Floyd-Warshall promising (answer: not really)
def golf(g,t):
    g=[[v+9e9*(v==0)for v in r]for r in g]
    n=list(range(len(g)))
    for k in n:
        for j in n:
            for i in n:
                g[i][j]=min(g[i][j],g[i][k]+g[k][j])
    return sum(g[i][i]for i in n if g[0][i]<=t)

assert golf([
    [0, 40, 0, 40, 0, 0],
    [40, 6, 0, 0, 40, 0],
    [0, 0, 3, 0, 15, 0],
    [40, 0, 0, 4, 40, 15],
    [0, 40, 15, 40, 1, 0],
    [0, 0, 0, 15, 0, 2]],
    80) == 13

assert golf([
    [ 0,  0, 40,  0, 40, 40,  0, 40,  0],
    [ 0,  1, 40,  0, 40,  0,  0,  0,  0],
    [40, 40,  1, 40,  0,  0,  0,  0,  0],
    [ 0,  0, 40,  1,  0, 40,  0,  0,  0],
    [40, 40,  0,  0,  1,  0, 40,  0,  0],
    [40,  0,  0, 40,  0,  1,  0,  0, 40],
    [ 0,  0,  0,  0, 40,  0,  1, 40,  0],
    [40,  0,  0,  0,  0,  0, 40,  1, 40],
    [ 0,  0,  0,  0,  0, 40,  0, 40,  1]],
    1000) == 8

