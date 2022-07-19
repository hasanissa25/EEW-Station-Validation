from typing import List

import pandas as pd
from pandas.core.frame import DataFrame


def convert_array_of_latency_objects_into_array_of_dataframes(
        array_of_latencies: list):
    columns = ('network', 'station', 'channel',
               'startTime', 'data_latency')
    array_of_latency_dataframes: List[DataFrame] = []
    for latency_object in array_of_latencies:
        array_of_latency_dataframes.append(pd.DataFrame(
            data=latency_object, index=columns).T)
    return array_of_latency_dataframes
