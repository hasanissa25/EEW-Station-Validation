'''
A module that contains utilities to extract latency values from HDF5 format
files and report on them
'''
import logging

import numpy as np
from typing import Any

from pandas.core.frame import DataFrame


def latencyreport(
        combined_latency_dataframe_for_all_days_dataframe: DataFrame,
        network: str,
        station: str,
        json_dict: dict,
        timely_threshold: float,
        timely_percent: float
) -> dict:
    '''
    Function to report on latency information about a station

    Parameters
    ----------
    typeofinstrument: str
        The instrument type that we are fetching data from: "APOLLO" / "GURALP"
    network: str
        The network code for the station
    station: str
        The station code to be reported on

    startdate: date
        The first date to check latency for

    enddate: date
        The last date to check latency for

    path: str
        The path to the directory that stores latency information for either \
            Guralp or Apollo instruments

    timely_threshold: float
        The latency goal in seconds that latency is expected to be below

    timely_percent: float
        The percentage of latency values that should be below the
        timely_threshold

    json_dict: str
        The dictionary object to store the results of the report in

    Returns
    -------
        dict: The dictionary object containing the results of the report
    '''
    # Collect the list of files to collect latency information from

    logging.info("Generating JSON report..")
    final_json_dict = populate_json_with_latency_info(
        json_dict=json_dict,
        combined_latency_dataframe_for_all_days_dataframe=combined_latency_dataframe_for_all_days_dataframe,  # noqa 501
        network=network,
        station=station,
        timely_threshold=timely_threshold,
        timely_percent=timely_percent,
    )
    return final_json_dict


def populate_json_with_latency_info(
        json_dict: dict,
        combined_latency_dataframe_for_all_days_dataframe: DataFrame,
        network: str,
        station: str,
        timely_threshold: float,
        timely_percent: float,
):

    channels = json_dict['channels'].keys()
    logging.debug(f'List of channels in the json_dict: {channels}')
    # Calculate average latency for the individual channels and\
    #  timely_percentage and failed latencies
    for channel in channels:
        average = combined_latency_dataframe_for_all_days_dataframe[
            combined_latency_dataframe_for_all_days_dataframe.channel
            == channel].data_latency.mean()
        logging.info(
            f'Average latency for channel {channel} is \
{round(float(average), 3)} seconds')  # :.3f
        json_dict['channels'][channel]['latency'] = {}
        json_dict['channels'][channel]['latency']['average_latency'] = \
            round(float(average), 2)
        below_threshold = percentbelowthreshold(
            f'{station}.{channel}',
            combined_latency_dataframe_for_all_days_dataframe
            [combined_latency_dataframe_for_all_days_dataframe.channel ==
             channel].data_latency,
            timely_threshold)
        json_dict['channels'][channel]['latency']['timely_availability'] = \
            round(float(below_threshold), 2)
        latencies_for_current_channel = \
            combined_latency_dataframe_for_all_days_dataframe[
                combined_latency_dataframe_for_all_days_dataframe.channel
                == channel]
        number_of_latencies_for_current_channel = \
            latencies_for_current_channel.data_latency.size
        number_of_failed_latencies_for_current_channel = \
            latencies_for_current_channel[
                latencies_for_current_channel["data_latency"] > 3]\
            .data_latency.size
        json_dict['channels'][channel]['latency']['total_latencies'] = \
            number_of_latencies_for_current_channel
        json_dict['channels'][channel]['latency']['failed_latencies'] = \
            number_of_failed_latencies_for_current_channel

    # JSON report calculations
    average = \
        combined_latency_dataframe_for_all_days_dataframe.data_latency.mean()
    logging.info(
        f'Overall average latency for {network}-{station} is \
{round(float(average), 2)} seconds')
    json_dict['station_latency'] = {}
    json_dict['station_latency']['average_latency'] = round(float(average), 2)
    below_threshold = percentbelowthreshold(
        station,
        combined_latency_dataframe_for_all_days_dataframe.data_latency,
        timely_threshold)
    json_dict['station_latency']['timely_availability'] = round(
        float(below_threshold), 2)
    if below_threshold >= timely_percent:
        json_dict['station_latency']['timely_passed'] = True
    else:
        json_dict['station_latency']['timely_passed'] = False
    return json_dict


def percentbelowthreshold(
    station: str,
    latencies: Any,
    threshold: float
) -> float:
    '''
    Function that calculates the percentage of values in an array of latency
    values that are below a specified threshold

    Parameters
    ----------
    station: string
        The code of the station that is being tested, for logging purposes
    latencies: Numpy Array
        The latency values to test against the threshold
    threshold: float
        The maximum latency to test against

    Returns
    -------
    float:
        The percentage of latency values that were below the threshold
    '''
    if(len(latencies) > 0):
        n = np.count_nonzero(latencies < threshold)
        percent = n / len(latencies) * 100
        return float(percent)
    else:
        logging.warning(
            "Skipping Timely Availability calculation. Please check the \
latency files.")
        return 0.0
