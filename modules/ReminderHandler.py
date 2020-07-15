from datetime import datetime
from datetime import timezone
import pytz

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
    eastern = pytz.timezone('US/Eastern')
    loc_dt = datetime.now(eastern)
    now = arrow.get(loc_dt)
    shift = (num - now.weekday()) % 7
    a = now.shift(days=+shift)
    s = a.format('MM:DD:YYYY')
    s = s + " " + time
    final = arrow.get(s, 'MM:DD:YYYY HH:mm')
    # Shift +4 to get UTC
    final = final.shift(hours=+4)
    # Shift -5 for the 5 hour reminder window
    final = final.shift(hours=-5)
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
    a = name_to_utc("Saturday", "19:00")
    print(a)
    seconds = convert_to_seconds(a)
    print(seconds)
