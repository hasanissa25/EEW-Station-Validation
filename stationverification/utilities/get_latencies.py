from typing import Any, List, Tuple
from datetime import date
from stationverification.utilities.get_latencies_from_apollo \
    import get_latencies_from_apollo
from stationverification.utilities.get_latencies_from_guralp import \
    get_latencies_from_guralp


def get_latencies(
    typeofinstrument: str,
    files: list,
    network: str,
    station: str,
    startdate=date,
    enddate=date
) -> Tuple:
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
        A list of Latency files to search, JSON for Apollo, CSV for Guralp

    Returns
    -------
    combined_latency_dataframe_for_all_days_dataframe: Dataframe
        A pandas DataFrame containing a list of latency values for the Station
    array_of_daily_latency_dataframes: list
        A list containing pandas latency dataframes for each day
    '''
    combined_latency_dataframe_for_all_days_dataframe: List[Any] = []
    array_of_daily_latency_objects_max_latency_only: List[Any] = []
    array_of_daily_latency_objects_all_latencies: List[Any] = []

    if typeofinstrument == "APOLLO":
        combined_latency_dataframe_for_all_days_dataframe,\
            array_of_daily_latency_objects_max_latency_only, \
            array_of_daily_latency_objects_all_latencies =\
            get_latencies_from_apollo(
                files=files,
                network=network,
                station=station)

    elif typeofinstrument == "GURALP":
        combined_latency_dataframe_for_all_days_dataframe, \
            array_of_daily_latency_objects_all_latencies =\
            get_latencies_from_guralp(
                files=files,
                startdate=startdate,
                enddate=enddate)
        array_of_daily_latency_objects_max_latency_only = \
            array_of_daily_latency_objects_all_latencies
    return combined_latency_dataframe_for_all_days_dataframe,\
        array_of_daily_latency_objects_max_latency_only,\
        array_of_daily_latency_objects_all_latencies
