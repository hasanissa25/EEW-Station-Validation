# flake8: noqa
from typing import Tuple
from datetime import date
from pandas.core.frame import DataFrame

from tests.latency.test_scripts.isolated_components.get_latencies_from_JSON import calculate_apollo_latencies


def getlatencies(
    typeofinstrument: str,
    files: list,
    network: str,
    station: str,
    startdate=date,
    enddate=date
) -> Tuple[DataFrame, list]:
    '''
    A function that returns a dataframe that includes 'network', 'station', \
        'channel', 'data_latency' columns given CSV or  JSON files

    Parameters
    ----------
    typeofinstrument: str
        The type of instrument the data was fetched from 'APOLLO' or 'GURALP'
    network: str
        The network code for the selected station
    station: str
        The station code for the selected station
    files: str
        A list of Latency files to search, JSON for Apollo, CSV for GUralp

    Returns
    -------
    combined_latency_dataframe_for_all_days: Dataframe
        A pandas DataFrame containing a list of latency values for the Station
    array_of_daily_latency_dataframes: list
        A list containing pandas latency dataframes for each day
    '''
    if typeofinstrument == "APOLLO":
        combined_latency_dataframe_for_all_days_dataframe,\
            array_of_daily_latency_dataframes = calculate_apollo_latencies(
                files=files,
                network=network,
                station=station)

    return combined_latency_dataframe_for_all_days_dataframe, \
        array_of_daily_latency_dataframes
