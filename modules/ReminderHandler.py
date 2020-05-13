from datetime import datetime

import arrow
from arrow import Arrow


def convert_to_seconds(a: Arrow):
    now = arrow.get(datetime.now())
    until = a - now
    return until.seconds


def name_to_utc(day: str, time: str):
    num = convert_day_to_num(day)
    now = arrow.get(datetime.now())
    shift = num - now.weekday()
    a = now.shift(days=+shift)
    s = a.format('MM:DD:YYYY')
    s = s + " " +time
    # the minus 1 is to make it 5 hours behind in EST, which is 1 hour behind in UTC
    final = arrow.get(s, 'MM:DD:YYYY HH:mm').shift(hours=-1)
    return final


def convert_day_to_num(day):
    if day == "Monday":
        num = 0
    elif day == "Tuesday":
        num = 1
    elif day == "Wednesday":
        num = 2
    elif day == "Thursday":
        num = 3
    elif day == "Friday":
        num = 4
    elif day == "Saturday":
        num = 5
    elif day == "Sunday":
        num = 6
    else:
        num = 6
    return num


if __name__ == '__main__':
    name_to_utc("Friday", "10:00")
