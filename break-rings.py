import itertools


def break_rings(ringLinks):
    ringIds = set.union(*ringLinks)

    for numRingsToBreak in range(1, len(ringIds)):
        for ringsToBreak in itertools.combinations(ringIds, numRingsToBreak):
            # if rings-to-break have some sort of overlap with all ring links,
            # then breaking those rings would get rid of all ring links;
            if all([set(ringsToBreak) & ringLink for ringLink in ringLinks]):
                return numRingsToBreak

    # should never get here
    return None


if __name__ == '__main__':
    print("in-file asserts begin")
    # These "asserts" using only for self-checking and not necessary for auto-testing
    assert break_rings(({1, 2}, {2, 3}, {3, 4}, {4, 5}, {5, 6}, {4, 6})) == 3, "example"
    assert break_rings(({1, 2}, {1, 3}, {1, 4}, {2, 3}, {2, 4}, {3, 4})) == 3, "All to all"
    assert break_rings(({5, 6}, {4, 5}, {3, 4}, {3, 2}, {2, 1}, {1, 6})) == 3, "Chain"
    assert break_rings(({8, 9}, {1, 9}, {1, 2}, {2, 3}, {3, 4}, {4, 5}, {5, 6}, {6, 7}, {8, 7})) == 5, "Long chain"
    print("in-file asserts end")

