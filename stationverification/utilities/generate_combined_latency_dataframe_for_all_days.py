from pandas import DataFrame
import pandas as pd


def generate_combined_latency_dataframe_for_all_days(
        list_of_latencies_for_all_days: list) -> DataFrame:
    latency_dataframe = pd.DataFrame(
        data=[])
    for latency in list_of_latencies_for_all_days:
        latency_dataframe = latency_dataframe.append(
            latency, ignore_index=True)
    return latency_dataframe
