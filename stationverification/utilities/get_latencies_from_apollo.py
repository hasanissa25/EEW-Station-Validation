import json
import logging

from typing import Any, List, Tuple

import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame

from stationverification.utilities import exceptions

# flake8: noqa


def get_latencies_from_apollo(files: list,
                              network: str,
                              station: str) -> Tuple[Any, Any, Any]:
    logging.info("Generating latencies from Apollo files...")
    combined_latency_data_for_all_days, \
        array_of_daily_latency_objects_max_latency_only,\
        array_of_daily_latency_objects_all_latencies = get_latencies_from_apollo_files(
            files=files, network=network, station=station)

    list_of_latencies_for_all_days = optimize_creating_list_of_latencies(
        latency_data=combined_latency_data_for_all_days)

    logging.info("Finished creating list of latencies for all days")

    return list_of_latencies_for_all_days, \
        array_of_daily_latency_objects_max_latency_only,\
        array_of_daily_latency_objects_all_latencies


def get_latencies_from_apollo_files(files: list,
                                    network: str,
                                    station: str) -> Tuple[Any, Any, Any]:
    # Storing the data of all the latency files
    combined_latency_data_for_all_days: dict = {}
    # Storing the data of all the latency files seperated into current day
    array_of_daily_latency_objects_max_latency_only: List[Any] = []
    array_of_daily_latency_objects_all_latencies: List[Any] = []
    for file in files:
        logging.info(f"Generating latency from: {file}")
        # Opening JSON file
        json_latency_file = open(file)
        try:
            latency_data = json.load(json_latency_file)
        except json.decoder.JSONDecodeError:
            raise exceptions.LatencyFileError(
                f'Problem detected in latency file: {file}')
        # Storing the data of the current days JSON latency file
        current_day_max_latencies: dict = {}
        current_day_all_latencies: dict = {}
        # Iterating through the json availability array which a string "id",
        # and an array of latency data "Intervals"
        for current_NSC in latency_data['availability']:
            current_id = current_NSC["id"]
            network_station = [network, station]

            # making sure we are looping over the required network station
            # combo, as the current iteration of the latency JSON files,
            # contained all the network and stations in one JSON file
            # for that specific day.
            if all(x in current_id for x in network_station):
                # splitting the id column and fetching the network, station
                # and channel values, id originally looks like the following :
                # "QW.QCC01.HNN"
                id_split = current_NSC['id'].split('.')
                if len(id_split) == 3:
                    current_network, current_station,\
                        current_channel = id_split
                elif len(id_split) == 4:
                    current_network, current_station, current_location,\
                        current_channel = id_split
                # looping over the intervals array, which contains all the
                # latency objects a specific NSC
                for current_latency in current_NSC['intervals']:
                    combined_latency_data_for_all_days, \
                        current_day_max_latencies, current_day_all_latencies \
                        = get_latency_value_for_current_timestamp(
                            current_latency=current_latency,
                            combined_latency_data_for_all_days=combined_latency_data_for_all_days,  # noqa
                            current_day_max_latencies=current_day_max_latencies,  # noqa
                            current_day_all_latencies=current_day_all_latencies,  # noqa
                            current_network=current_network,
                            current_station=current_station,
                            current_channel=current_channel)
        json_latency_file.close()

        array_of_daily_latency_objects_max_latency_only.append(
            current_day_max_latencies)

        array_of_daily_latency_objects_all_latencies.append(
            current_day_all_latencies)
    return combined_latency_data_for_all_days, \
        array_of_daily_latency_objects_max_latency_only,\
        array_of_daily_latency_objects_all_latencies


def optimize_creating_list_of_latencies(latency_data: dict) -> list:
    list_of_combined_latencies = []
    for key, value in latency_data.items():
        list_of_combined_latencies.append(np.float16(value["data_latency"]))
    return list_of_combined_latencies


def create_latency_dataframe_from_csv_file(path_to_csv_file: str) -> DataFrame:
    combined_latency_dataframe_for_all_days_dataframe = pd.DataFrame(
        {'network': [], 'station': [], 'channel': [], "startTime": [],
         'data_latency': []})
    combined_latency_dataframe_for_all_days_dataframe = pd.read_csv(
        path_to_csv_file, dtype={'data_latency': np.float16})

    return combined_latency_dataframe_for_all_days_dataframe


def get_latency_value_for_current_timestamp(current_latency: dict,
                                            combined_latency_data_for_all_days:
                                            dict,
                                            current_day_max_latencies: dict,
                                            current_day_all_latencies: dict,
                                            current_network: str,
                                            current_station: str,
                                            current_channel: str) -> \
        Tuple[dict, dict, dict]:
    if current_latency["retx"]["allPackets"] == 1:
        if current_latency["latency"]["maximum"] != -1:
            append_to_latency_objects(
                append_to_current_day_max_latencies=True,
                append_to_combined_latency_data_for_all_days=True,
                append_to_current_day_all_latencies=True,
                current_latency=current_latency["latency"]["maximum"],
                combined_latency_data_for_all_days=combined_latency_data_for_all_days,  # noqa
                current_day_max_latencies=current_day_max_latencies,
                current_day_all_latencies=current_day_all_latencies,
                current_network=current_network,
                current_station=current_station,
                current_channel=current_channel,
                start_time=current_latency[
                    'startTime'],
                packet_id="max")

    elif current_latency["retx"]["allPackets"] == 2:
        if current_latency["latency"]["maximum"] != -1:
            append_to_latency_objects(
                append_to_current_day_max_latencies=True,
                append_to_combined_latency_data_for_all_days=True,
                append_to_current_day_all_latencies=True,
                current_latency=current_latency["latency"]["maximum"],
                combined_latency_data_for_all_days=combined_latency_data_for_all_days,  # noqa
                current_day_max_latencies=current_day_max_latencies,
                current_day_all_latencies=current_day_all_latencies,
                current_network=current_network,
                current_station=current_station,
                current_channel=current_channel,
                start_time=current_latency[
                    'startTime'],
                packet_id="max")

        if current_latency["latency"]["minimum"] != -1:
            append_to_latency_objects(
                append_to_current_day_max_latencies=False,
                append_to_combined_latency_data_for_all_days=True,
                append_to_current_day_all_latencies=True,
                current_latency=current_latency["latency"]["minimum"],
                combined_latency_data_for_all_days=combined_latency_data_for_all_days,  # noqa
                current_day_max_latencies=current_day_max_latencies,
                current_day_all_latencies=current_day_all_latencies,
                current_network=current_network,
                current_station=current_station,
                current_channel=current_channel,
                start_time=current_latency[
                    'startTime'],
                packet_id="min")

    elif current_latency["retx"]["allPackets"] == 3:
        if current_latency["latency"]["maximum"] != -1:
            append_to_latency_objects(
                append_to_current_day_max_latencies=True,
                append_to_combined_latency_data_for_all_days=True,
                append_to_current_day_all_latencies=True,
                current_latency=current_latency["latency"]["maximum"],
                combined_latency_data_for_all_days=combined_latency_data_for_all_days,  # noqa
                current_day_max_latencies=current_day_max_latencies,
                current_day_all_latencies=current_day_all_latencies,
                current_network=current_network,
                current_station=current_station,
                current_channel=current_channel,
                start_time=current_latency[
                    'startTime'],
                packet_id="max")

        if current_latency["latency"]["minimum"] != -1:
            append_to_latency_objects(
                append_to_current_day_max_latencies=False,
                append_to_combined_latency_data_for_all_days=True,
                append_to_current_day_all_latencies=True,
                current_latency=current_latency["latency"]["minimum"],
                combined_latency_data_for_all_days=combined_latency_data_for_all_days,  # noqa
                current_day_max_latencies=current_day_max_latencies,
                current_day_all_latencies=current_day_all_latencies,
                current_network=current_network,
                current_station=current_station,
                current_channel=current_channel,
                start_time=current_latency[
                    'startTime'],
                packet_id="min")

        if current_latency["latency"]["average"] != -1:
            calculated_unkown_latency_value_prep = 3 * \
                current_latency["latency"]["average"]
            calculated_unkown_latency_value = calculated_unkown_latency_value_prep - current_latency["latency"]["minimum"] - current_latency["latency"]["maximum"]  # noqa
            append_to_latency_objects(
                append_to_current_day_max_latencies=False,
                append_to_combined_latency_data_for_all_days=True,
                append_to_current_day_all_latencies=True,
                current_latency=calculated_unkown_latency_value,
                combined_latency_data_for_all_days=combined_latency_data_for_all_days,  # noqa
                current_day_max_latencies=current_day_max_latencies,
                current_day_all_latencies=current_day_all_latencies,
                current_network=current_network,
                current_station=current_station,
                current_channel=current_channel,
                start_time=current_latency[
                       'startTime'],
                packet_id="average")

    elif current_latency["retx"]["allPackets"] > 3:
        if current_latency["latency"]["maximum"] != -1:
            append_to_latency_objects(
                append_to_current_day_max_latencies=True,
                append_to_combined_latency_data_for_all_days=True,
                append_to_current_day_all_latencies=True,
                current_latency=current_latency["latency"]["maximum"],
                combined_latency_data_for_all_days=combined_latency_data_for_all_days,  # noqa
                current_day_max_latencies=current_day_max_latencies,
                current_day_all_latencies=current_day_all_latencies,
                current_network=current_network,
                current_station=current_station,
                current_channel=current_channel,
                start_time=current_latency[
                    'startTime'],
                packet_id="max")

        if current_latency["latency"]["minimum"] != -1:
            append_to_latency_objects(
                append_to_current_day_max_latencies=False,
                append_to_combined_latency_data_for_all_days=True,
                append_to_current_day_all_latencies=True,
                current_latency=current_latency["latency"]["minimum"],
                combined_latency_data_for_all_days=combined_latency_data_for_all_days,  # noqa
                current_day_max_latencies=current_day_max_latencies,
                current_day_all_latencies=current_day_all_latencies,
                current_network=current_network,
                current_station=current_station,
                current_channel=current_channel,
                start_time=current_latency[
                    'startTime'],
                packet_id="min")

        if current_latency["latency"]["average"] != -1:
            number_of_times_to_append_to_latencies = current_latency["retx"]["allPackets"] - 2
            for iteration in range(number_of_times_to_append_to_latencies):
                append_to_latency_objects(
                    append_to_current_day_max_latencies=False,
                    append_to_combined_latency_data_for_all_days=True,
                    append_to_current_day_all_latencies=True,
                    current_latency=current_latency["latency"]["average"],
                    combined_latency_data_for_all_days=combined_latency_data_for_all_days,  # noqa
                    current_day_max_latencies=current_day_max_latencies,
                    current_day_all_latencies=current_day_all_latencies,
                    current_network=current_network,
                    current_station=current_station,
                    current_channel=current_channel,
                    start_time=current_latency[
                        'startTime'],
                    packet_id=f"average{iteration+1}")
    return combined_latency_data_for_all_days,\
        current_day_max_latencies, \
        current_day_all_latencies


def append_to_latency_objects(
        append_to_current_day_max_latencies: bool,
        append_to_combined_latency_data_for_all_days: bool,
        append_to_current_day_all_latencies: bool,
        current_latency: float,
        combined_latency_data_for_all_days: dict,
        current_day_max_latencies: dict,
        current_day_all_latencies: dict,
        current_network: str,
        current_station: str,
        current_channel: str,
        start_time: str,
        packet_id: str):
    # One dataframe that holds all the latency data, used in Latency Log plot
    if append_to_combined_latency_data_for_all_days is True:
        combined_latency_data_for_all_days[current_network +
                                           "."+current_station
                                           +
                                           "."+current_channel
                                           +
                                           "." + start_time
                                           +
                                           "." + packet_id] = {'network':
                                                               current_network,
                                                               'station':
                                                               current_station,
                                                               'channel':
                                                               current_channel,
                                                               'startTime':
                                                               start_time,
                                                               'data_latency':
                                                               current_latency
                                                               }
    if append_to_current_day_all_latencies is True:
        # An array of dataframes, for each day in the validation period. \
        # Has all the latency values for that day, used in \
        # timely_availability_plot
        current_day_all_latencies[current_network +
                                  "."+current_station +
                                  "."+current_channel +
                                  "." +
                                  start_time +
                                  "." + packet_id] = {'network': current_network,
                                                      'station': current_station,
                                                      'channel': current_channel,
                                                      'startTime': start_time,
                                                      'data_latency':
                                                      current_latency
                                                      }
    if append_to_current_day_max_latencies is True:
        # An array of dataframes, for each day in the validation period. \
        # Only includes the max latency values, used in the latency line plot
        current_day_max_latencies[current_network +
                                  "."+current_station +
                                  "."+current_channel +
                                  "." +
                                  start_time +
                                  "." + packet_id] = {'network': current_network,
                                                      'station': current_station,
                                                      'channel': current_channel,
                                                      'startTime': start_time,
                                                      'data_latency':
                                                      current_latency
                                                      }
