
import math

GREGORIAN_EPOCH = 1721425.5
PERSIAN_EPOCH = 1948320.5

# USAGE :
    # j = gregorian_to_jd(year, mon , mday)
    # julian_day_to_persian(j)


# Algorithm came from http://www.fourmilab.ch/documents/calendar/


def create_persian_date(date):

    julian_day      = _gregorian_to_julian_day(date.year, date.month, date.day)
    persian_date    = _julian_day_to_persian(julian_day)

    return persian_date


def create_gregorian_date(year, month, day):

    julian_day      = _persian_to_julian_day(year, month,day)
    gregorian_date  = _julian_day_to_gregorian(julian_day)

    return  gregorian_date


def _check_leap(year):
    """
        Checks to see whether the gregorian year is a leap year or not
    """

    return ((year % 4) == 0) and (not(((year % 100) == 0) and ((year % 400) != 0)))


def _gregorian_to_julian_day(year, month, day):
    """
        Converts Gregorian Date to Julian Day
    """
    if month <= 2:
        val = 0
    else:
        val = -1 if _check_leap(year) else -2

    julian_day = (GREGORIAN_EPOCH - 1) + 365 * (year - 1)
    julian_day += math.floor((year - 1) / 4)
    julian_day += (-math.floor((year - 1) / 100)) + math.floor((year - 1) / 400)
    julian_day += math.floor((((367 * month) - 362) / 12) + val) + day
    return julian_day


def _julian_day_to_gregorian(jd):
    """
        Converts to Julian Day to Gregorian Date
    """
    wjd = math.floor(jd - 0.5) + 0.5
    depoch = wjd - GREGORIAN_EPOCH
    quadricent = math.floor(depoch / 146097)
    dqc = _mod(depoch, 146097)
    cent = math.floor(dqc / 36524)
    dcent = _mod(dqc, 36524)
    quad = math.floor(dcent / 1461)
    dquad = _mod(dcent, 1461)
    yindex = math.floor(dquad / 365)
    year = (quadricent * 400) + (cent * 100) + (quad * 4) + yindex
    if not ((cent == 4) or (yindex == 4)):
        year += 1

    yearday = wjd - _gregorian_to_julian_day(year, 1, 1)

    if wjd < _gregorian_to_julian_day(year, 3, 1):
        leapadj = 0
    elif _check_leap(year):
        leapadj =1
    else:
        leapadj = 2

    month = math.floor((((yearday + leapadj) * 12) + 373) / 367)
    day = (wjd - _gregorian_to_julian_day(year, month, 1)) + 1

    return int(year), int(month), int(day)



def _mod(a, b):
    return a - (b * math.floor(a / b))


def _julian_day_to_persian(jd):
    """
    Converts Julian Day To Persian Date
    """
    jd = math.floor(jd) + 0.5
    depoch = jd - _persian_to_julian_day(475, 1, 1)
    cycle = math.floor(depoch / 1029983)
    cyear = _mod(depoch, 1029983)
    if cyear == 1029982 :
        ycycle = 2820
    else:
        aux1 = math.floor(cyear / 366)
        aux2 = _mod(cyear, 366)
        ycycle = math.floor(((2134 * aux1) + (2816 * aux2) + 2815) / 1028522) + aux1 + 1

    year = ycycle + (2820 * cycle) + 474
    if year <= 0:
        year -= 1

    yday = (jd - _persian_to_julian_day(year, 1, 1)) + 1

    if yday <= 186 :
        month = math.ceil(yday/31)
    else:
        month = math.ceil((yday - 6) / 30)

    day = (jd - _persian_to_julian_day(year, month, 1)) + 1

    return (int(year), int(month), int(day))


def _persian_to_julian_day(year, month, day):
    """
        Converts Persian Date to Julian Day
    """
    if year >= 0:
        epbase = year - 474
    else:
        epbase = year - 473
    epyear = 474 + _mod(epbase, 2820)

    if month <= 7:
        tmp = (month - 1) * 31
    else:
        tmp = (month - 1) * 30 + 6


    return_value = day + tmp + math.floor(((epyear * 682) - 110) / 2816)
    return_value += (epyear - 1) * 365 + math.floor(epbase / 2820) * 1029983
    return_value += (PERSIAN_EPOCH - 1)

    return return_value
