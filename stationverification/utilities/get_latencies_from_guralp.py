from typing import Tuple
from datetime import date, timedelta

import pandas as pd
from pandas.core.frame import DataFrame


def get_latencies_from_guralp(files: list,
                              startdate: date,
                              enddate: date) -> \
        Tuple[DataFrame, list]:
    combined_latency_dataframe_for_all_days_dataframe = pd.DataFrame(
        {'network': [], 'station': [], 'channel': [], "startTime": [],
         'data_latency': []})
    array_of_daily_latency_objects = []
    for file in files:
        current_file_dataframe = pd.read_csv(file)

        current_file_dataframe[['network', 'station', "location", 'channel']
                               ] = \
            current_file_dataframe['channel'].str.split('.',
                                                        expand=True)

        current_file_dataframe.rename(
            columns={"channel": "channel",
                     "network latency": "network_latency",
                     "data latency": "data_latency",
                     "network": "network",
                     "station": "station",
                     "location": "location",
                     "timestamp": "startTime"}, inplace=True)
        # Data_latency column is in the format of  "=269/100+6.6", which we \
        # need to split and get the value for
        current_file_dataframe[['data_latency']] = \
            current_file_dataframe['data_latency'].str.extract(
            '=(.*)/').astype(float)/100
        current_file_dataframe['data_latency'] = \
            current_file_dataframe['network_latency'] + \
            current_file_dataframe['data_latency']
        combined_latency_dataframe_for_all_days_dataframe = \
            combined_latency_dataframe_for_all_days_dataframe.append(
                current_file_dataframe[[
                    'network', 'station', 'channel', 'startTime',
                    'data_latency']], sort=False)
    # Populating the daily latency array by looping over the dates in the
    # validation period, and filtering the
    # combined_latency_dataframe_for_all_days_dataframe to only those dates,
    # then creating a dataframe with that dates data
    # We then add that dates dataframe into the daily latency array

    # Adding a column that represents the start time in a YY-MM-DD format, in
    # order to compare it to the current date we are looping over
    combined_latency_dataframe_for_all_days_dataframe_with_datetime = \
        combined_latency_dataframe_for_all_days_dataframe
    combined_latency_dataframe_for_all_days_dataframe_with_datetime["date"] =\
        pd.to_datetime(
        combined_latency_dataframe_for_all_days_dataframe["startTime"],
        infer_datetime_format=True).apply(lambda x: x.strftime('%Y-%m-%d'))

    while startdate < enddate:
        array_of_daily_latency_objects.append(
            combined_latency_dataframe_for_all_days_dataframe_with_datetime[
                combined_latency_dataframe_for_all_days_dataframe_with_datetime["date"]  # noqa
                == str(startdate)])
        startdate += timedelta(days=+1)

    if 'date' in\
            combined_latency_dataframe_for_all_days_dataframe_with_datetime.columns:  # noqa
        combined_latency_dataframe_for_all_days_dataframe_with_datetime.drop(
            'date', axis=1, inplace=True)
    return combined_latency_dataframe_for_all_days_dataframe, \
        array_of_daily_latency_objects
