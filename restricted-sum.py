def checkio(data):
    if data:
        return data[0] + checkio(data[1:])
    return 0
