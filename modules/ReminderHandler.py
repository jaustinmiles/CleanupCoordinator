from datetime import datetime

import arrow
from arrow import Arrow


def convert_to_seconds(a: Arrow):
    now = arrow.get(datetime.now())
    until = a - now
    if until.days:
        s = until.days * 86400 + until.seconds
    else:
        s = until.seconds
    return s


def name_to_utc(day: str, time: str):
    num = convert_day_to_num(day)
    now = arrow.get(datetime.now())
    shift = num - now.weekday()
    a = now.shift(days=+shift)
    s = a.format('MM:DD:YYYY')
    s = s + " " + time
    # the minus 1 is to make it 5 hours behind in EST, which is 1 hour behind in UTC
    final = arrow.get(s, 'MM:DD:YYYY HH:mm').shift(hours=-1)
    return final


def convert_day_to_num(day):
    day = day.lower().strip()
    if day == "monday":
        num = 0
    elif day == "tuesday":
        num = 1
    elif day == "wednesday":
        num = 2
    elif day == "thursday":
        num = 3
    elif day == "friday":
        num = 4
    elif day == "saturday":
        num = 5
    elif day == "sunday":
        num = 6
    else:
        num = 6
    return num


if __name__ == '__main__':
    a = name_to_utc("Friday", "10:00")
    seconds = convert_to_seconds(a)
    print(seconds)
