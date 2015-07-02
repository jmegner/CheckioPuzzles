def checkio(data):
    masterPoint = data[0]
    area = 0

    for point1, point2 in zip(data[1:-1], data[2:]):
        area += triangleArea(
            masterPoint[0], masterPoint[1],
            point1[0], point1[1],
            point2[0], point2[1])

    return area


def crossProduct(x1, y1, x2, y2):
    return x1 * y2 - x2 * y1


def triangleArea(x1, y1, x2, y2, x3, y3):
    return abs(crossProduct(x2 - x1, y2 - y1, x3 - x2, y3 - y2)) / 2


if __name__ == '__main__':
    #This part is using only for self-checking and not necessary for auto-testing
    def almost_equal(checked, correct, significant_digits=1):
        precision = 0.1 ** significant_digits
        return correct - precision < checked < correct + precision

    assert almost_equal(
        checkio([[1, 1], [9, 9], [9, 1]]),
        32), "The half of the square"
    assert almost_equal(checkio(
        [[4, 10], [7, 1], [1, 4]]),
        22.5), "Triangle"
    assert almost_equal(checkio(
        [[1, 2], [3, 8], [9, 8], [7, 1]]),
        40), "Quadrilateral"
    assert almost_equal(checkio(
        [[3, 3], [2, 7], [5, 9], [8, 7], [7, 3]]),
        26), "Pentagon"
    assert almost_equal(checkio(
        [[7, 2], [3, 2], [1, 5], [3, 9], [7, 9], [9, 6]]),
        42), "Hexagon"
    assert almost_equal(checkio(
        [[4, 1], [3, 4], [3, 7], [4, 8], [7, 9], [9, 6], [7, 1]]),
        35.5), "Heptagon"

