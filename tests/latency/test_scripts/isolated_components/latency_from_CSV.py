# This script is to test fetching latency data from a CSV file
import pandas as pd
from datetime import date, timedelta

# flake8: noqa


def test_latency_from_CSV(typeofinstrument: str,
                          files: list,
                          network: str,
                          station: str,
                          startdate: date,
                          enddate: date):
    # Dataframe used to hold latency information for the station
    combined_latency_dataframe_for_all_days = pd.DataFrame(
        {'network': [], 'station': [], 'channel': [], "startTime": [], 'data_latency': []})
    array_of_daily_latency_dataframes = []
    if typeofinstrument == "GURALP":
        for file in files:
            # current_day_latency_data = {}
            current_file_dataframe = pd.read_csv(file)

            current_file_dataframe[['network', 'station', "location", 'channel']
                                   ] = current_file_dataframe['channel'].str.split('.',
                                                                                   expand=True)

            current_file_dataframe[['data latency']
                                   ] = current_file_dataframe['network latency']

            current_file_dataframe.rename(columns={"channel": "channel",
                                                   "network latency": "network_latency",
                                                   "data latency": "data_latency",
                                                   "network": "network",
                                                   "station": "station",
                                                   "location": "location",
                                                   "timestamp": "startTime"}, inplace=True)
            combined_latency_dataframe_for_all_days = combined_latency_dataframe_for_all_days.append(
                current_file_dataframe[['network', 'station', 'channel', 'startTime', 'data_latency']], sort=False)  # noqa: E501

        # Populating the daily latency array by looping over the dates in the validation period, \
        # and filtering the combined_latency_dataframe_for_all_days to only those dates, \
        # then creating a dataframe with that dates data
        # We then add that dates dataframe into the daily latency array

        # Adding a column that represents the start time in a YY-MM-DD format, in order to compare it to the current date we are looping over
        combined_latency_dataframe_for_all_days_with_datetime = combined_latency_dataframe_for_all_days
        combined_latency_dataframe_for_all_days_with_datetime["date"] = pd.to_datetime(
            combined_latency_dataframe_for_all_days["startTime"], infer_datetime_format=True).apply(lambda x: x.strftime('%Y-%m-%d'))

        while startdate < enddate:
            array_of_daily_latency_dataframes.append(combined_latency_dataframe_for_all_days_with_datetime[combined_latency_dataframe_for_all_days_with_datetime["date"] == str(
                startdate)])
            startdate += timedelta(days=+1)

        if 'date' in combined_latency_dataframe_for_all_days_with_datetime.columns:
            combined_latency_dataframe_for_all_days_with_datetime.drop(
                'date', axis=1, inplace=True)

    return combined_latency_dataframe_for_all_days, array_of_daily_latency_dataframes
