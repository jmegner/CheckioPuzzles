'''
author: Jacob Egner
date: 2015-07-14
island: mine

puzzle prompt:
http://www.checkio.org/mission/painting-wall

puzzle prompt source repo:
https://github.com/cielavenir/checkio-task-painting-wall

my checkio solution repo:
https://github.com/jmegner/CheckioPuzzles

'''


import collections


class Span(collections.namedtuple("Span", ["lo", "hi"])):

    def overlaps(self, other):
        return (
            self.lo <= other.lo <= self.hi
            or self.lo <= other.hi <= self.hi
            or other.lo <= self.lo <= other.hi
            or other.lo <= self.hi <= other.hi
        )


    def extended(self, other):
        return Span(min(self.lo, other.lo), max(self.hi, other.hi))


def checkio(metersRequired, plannedPaintOperations):
    paintedSpans = set()

    for planIdx, plannedPaintOperation in enumerate(plannedPaintOperations):
        addSpan(paintedSpans, Span(*plannedPaintOperation))
        metersPainted = sum(map(lambda span: span.hi - span.lo + 1, paintedSpans))

        if metersPainted >= metersRequired:
            return planIdx + 1

    return -1


def addSpan(spans, newSpan):
    overlappingSpans = []

    for span in spans:
        if span.overlaps(newSpan):
            overlappingSpans.append(span)

    for overlappingSpan in overlappingSpans:
        spans.remove(overlappingSpan)
        newSpan = newSpan.extended(overlappingSpan)

    spans.add(newSpan)


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert checkio(5, [[1, 5], [11, 15], [2, 14], [21, 25]]) == 1, "1st"
    assert checkio(6, [[1, 5], [11, 15], [2, 14], [21, 25]]) == 2, "2nd"
    assert checkio(11, [[1, 5], [11, 15], [2, 14], [21, 25]]) == 3, "3rd"
    assert checkio(16, [[1, 5], [11, 15], [2, 14], [21, 25]]) == 4, "4th"
    assert checkio(21, [[1, 5], [11, 15], [2, 14], [21, 25]]) == -1, "not enough"
    assert checkio(1000000011, [[1, 1000000000], [11, 1000000010]]) == -1, "large"
    assert checkio(30,[[1,2],[20,30],[25,28],[5,10],[4,21],[1,6]]) == 6, "test_2_4"

