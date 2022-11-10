import logging
import subprocess

from typing import List
from datetime import date, timedelta

from stationverification.utilities.julian_day_converter import \
    datetime_to_year_and_julian_day


def get_latency_files(
    typeofinstrument: str,
    network: str,
    path: str,
    station: str,
    startdate: date,
    enddate: date,

) -> List[str]:
    '''
    Find a list of the latency files for the given time period, network, and \
        station, for either Guralp or Apollo data

    Parameters
    ----------
    typeofinstrument: str
        The type of instrument the data was fetched from 'APOLLO' or 'GURALP'

    network: str
        The network that will be found in the latency file name

    station: str
        The station that will be found in the latency file name

    path: str
        The path to the latency data storage.

    startdate: date
        The date for the beginning of the test.

    enddate: date
        The last date of the test.

    Returns
    -------
    list:
        A list of the files for the specified date range
    '''
    files: list = []
    iterdate = startdate
    # Iterate through all the dates in the verification period and collect a
    # list of the associated files
    while iterdate < enddate:
        logging.debug(f'Looking for files for date {iterdate}')
        if typeofinstrument.lower() == "titansma":
            cmd = f'ls {path}/{iterdate.strftime("%Y/%m/%d")}/\
{network}.{station}.\
{datetime_to_year_and_julian_day(iterdate, typeofinstrument)}.json 2>/dev/null'
        elif typeofinstrument.lower() == "fortimus":
            cmd = f'ls {path}/{iterdate.strftime("%Y/%m/%d")}/{network}_\
{station}_*_H??_\
{datetime_to_year_and_julian_day(iterdate, typeofinstrument)}.csv \
2>/dev/null'

        output = subprocess.getoutput(
            cmd
        ).split('\n')

        if not output == ['']:
            files.extend(output)
        else:
            logging.warning(f'No Latency file found for {iterdate}')
        iterdate += timedelta(days=+1)

    # Throw an exception if no files in the time period are found
    if len(files) <= 0:
        raise FileNotFoundError(f'No files found in {path} for dates between \
{startdate} and {enddate}')
    logging.debug(f'List of files found: {files}')
    return files
