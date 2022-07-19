from datetime import date, datetime

from stationverification.utilities.julian_day_converter import \
    datetime_to_julian_day, datetime_to_year, datetime_to_month,\
    datetime_to_year_and_julian_day, datestring_to_julian_day, \
    year_and_julian_day_to_date

# flake8: noqa


def test_datetime_to_julian_day(test_date_1_digit: date,
                                test_date_2_digits: date,
                                test_date_3_digits: date
                                ):
    assert datetime_to_julian_day(test_date_1_digit) == "009"
    assert datetime_to_julian_day(test_date_2_digits) == "024"
    assert datetime_to_julian_day(test_date_3_digits) == "114"


def test_datetime_to_year(test_date_1_digit: date,
                          test_date_2_digits: date,
                          test_date_3_digits: date
                          ):
    assert datetime_to_year(test_date_1_digit) == "2022"
    assert datetime_to_year(test_date_2_digits) == "2022"
    assert datetime_to_year(test_date_3_digits) == "2022"


def test_datetime_to_month(test_date_1_digit: date,
                           test_date_month_2_digits: date,
                           ):
    assert datetime_to_month(test_date_1_digit) == "01"
    assert datetime_to_month(test_date_month_2_digits) == "11"


def test_datetime_to_year_and_julian_day(test_date_1_digit: date,
                                         test_date_2_digits: date,
                                         test_date_3_digits: date
                                         ):
    assert datetime_to_year_and_julian_day(
        test_date_1_digit, "APOLLO") == "2022.009"
    assert datetime_to_year_and_julian_day(
        test_date_2_digits, "APOLLO") == "2022.024"
    assert datetime_to_year_and_julian_day(
        test_date_3_digits, "APOLLO") == "2022.114"
    assert datetime_to_year_and_julian_day(
        test_date_1_digit, "GURALP") == "2022_009"
    assert datetime_to_year_and_julian_day(
        test_date_2_digits, "GURALP") == "2022_024"
    assert datetime_to_year_and_julian_day(
        test_date_3_digits, "GURALP") == "2022_114"


def test_datestring_to_julian_day():
    assert datestring_to_julian_day("2022-1-5") == "005"
    assert datestring_to_julian_day("2022-1-10") == "010"
    assert datestring_to_julian_day("2022-5-12") == "132"


def test_year_and_julian_day_to_date():
    assert year_and_julian_day_to_date("20221") == date(2022, 1, 1)
    assert year_and_julian_day_to_date("202210") == date(2022, 1, 10)
    assert year_and_julian_day_to_date("2022100") == date(2022, 4, 10)
