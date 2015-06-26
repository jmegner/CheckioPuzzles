def checkio(attempts):
    bestDivisors = {9, 8, 7, 5}
    numIsPossible = [False] + ([True] * 100)

    for (remainder, divisor) in attempts:
        bestDivisors.discard(divisor)
        for num in range(len(numIsPossible)):
            if num % divisor != remainder:
                numIsPossible[num] = False

    guess = numIsPossible.index(True)
    nextDivisor = max(bestDivisors)
    return (nextDivisor, guess)


if __name__ == '__main__':
    #This part is using only for self-checking and not necessary for auto-testing
    MAX_ATTEMPT = 8

    def initial_referee(data):
        data["attempt_count"] = 0
        data["guess"] = 0
        return data

    def check_solution(func, goal, initial):
        prev_steps = [initial]
        for attempt in range(MAX_ATTEMPT):
            divisor, guess = func(prev_steps[:])
            if guess == goal:
                return True
            if divisor <= 1 or divisor > 10:
                print("You gave wrong divisor range.")
                return False
            if guess < 1 or guess > 100:
                print("You gave wrong guess number range.")
                return False
            prev_steps.append((goal % divisor, divisor))
        print("Too many attempts.")
        return False

    assert check_solution(checkio, 47, (2, 5)), "1st example"
    assert check_solution(checkio, 94, (3, 7)), "1st example"
    assert check_solution(checkio, 52, (0, 2)), "1st example"
