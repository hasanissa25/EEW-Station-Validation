import datetime


def datetime_to_julian_day(date: datetime.date) -> str:
    '''
        date: a datetime.date object

        Returns the Julian day from the given date time object to 3 digits\
            '005' or '012' or '365'
    '''
    standard_date = date.timetuple()
    julian_day = standard_date.tm_yday
    if julian_day < 10:
        julianday = f"00{julian_day}"
    elif julian_day < 100:
        julianday = f"0{julian_day}"
    else:
        julianday = f'{julian_day}'
    return f'{julianday}'


def datetime_to_year(date: datetime.date) -> str:
    '''
        date: a datetime.date object

        Returns the year from the given date time object '2018'
    '''
    return f'{date.year}'


def datetime_to_month(date: datetime.date) -> str:
    '''
        date: a datetime.date object

        Returns the month from the given date time object to 2 digits;\
             '01' or '12'
    '''
    if date.month < 10:
        return "0" + str(date.month)
    else:
        return f'{date.month}'


def datetime_to_year_and_julian_day(
        date: datetime.date,
        instrumentType: str) -> str:
    '''
        date: a datetime.date object

        Returns the year and the Julian day from the given date time object to\
             3 digits '2018_005' or '2018_012' or '2018_365'
    '''
    standard_date = date.timetuple()
    julian_day = standard_date.tm_yday
    if julian_day < 10:
        julian_day_with_added_zeroes = str(f"00{julian_day}")
    elif julian_day < 100:
        julian_day_with_added_zeroes = str(f"0{julian_day}")
    else:
        julian_day_with_added_zeroes = f"{julian_day}"
    # Splitting it up as the Apollo file names might be different than Guralp
    if instrumentType == "APOLLO":
        formated_julian_day = f'{date.year}.{julian_day_with_added_zeroes}'
    elif instrumentType == "GURALP":
        formated_julian_day = f'{date.year}_{julian_day_with_added_zeroes}'
    return formated_julian_day


def datestring_to_julian_day(date_string: str) -> str:
    '''
        date_string: a string representing a date in the format of\
            'YYYY-MM-DD'; '2022-5-12'
        Returns the Julian day from the given date string to 3 digits\
            '005' or '012' or '365'
    '''
    format = '%Y-%m-%d'
    standard_date = datetime.datetime.strptime(date_string, format)
    julian_day = standard_date.timetuple().tm_yday
    if julian_day < 10:
        julian_day_with_added_zeroes = f"00{julian_day}"
    elif julian_day < 100:
        julian_day_with_added_zeroes = f"0{julian_day}"
    else:
        julian_day_with_added_zeroes = f"{julian_day}"
    return julian_day_with_added_zeroes


def year_and_julian_day_to_date(jdate: str) -> datetime.date:
    '''
        jdate: a string representing a date in the format of\
            'YYYYJulianDay'; '2018355'
        Returns a datetime object from the given year and julian day
    '''
    format = '%Y%j'
    standard_date = datetime.datetime.strptime(jdate, format).date()
    return standard_date
