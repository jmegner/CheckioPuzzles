def total_cost(calls):
    totalCost = 0
    dayMinutes = 0
    currentDate = ""
    secondsPerMinute = 60

    for call in calls:
        date, time, durationStr = call.split(' ')
        durationSeconds = int(durationStr)

        if date != currentDate:
            totalCost += costForDay(dayMinutes)
            dayMinutes = 0
            currentDate = date

        dayMinutes += ((durationSeconds + secondsPerMinute - 1)
            // secondsPerMinute)

    totalCost += costForDay(dayMinutes)

    return totalCost


def costForDay(minutes):
    minuteThreshold = 100
    lowerRate = 1
    upperRate = 2

    if minutes <= minuteThreshold:
        return minutes * lowerRate
    return minuteThreshold * lowerRate + (minutes - minuteThreshold) * upperRate


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert total_cost(("2014-01-01 01:12:13 181",
                       "2014-01-02 20:11:10 600",
                       "2014-01-03 01:12:13 6009",
                       "2014-01-03 12:13:55 200")) == 124, "Base example"
    assert total_cost(("2014-02-05 01:00:00 1",
                       "2014-02-05 02:00:00 1",
                       "2014-02-05 03:00:00 1",
                       "2014-02-05 04:00:00 1")) == 4, "Short calls but money..."
    assert total_cost(("2014-02-05 01:00:00 60",
                       "2014-02-05 02:00:00 60",
                       "2014-02-05 03:00:00 60",
                       "2014-02-05 04:00:00 6000")) == 106, "Precise calls"
