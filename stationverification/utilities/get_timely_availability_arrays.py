import arrow

from datetime import date
from pandas.core.frame import DataFrame
from typing import List, Tuple


def get_timely_availability_arrays(
    latencies: DataFrame, threshold: float
) -> Tuple[list, list, list, list]:
    HNN_timely_availability_percentage_array: List[float] = []
    HNE_timely_availability_percentage_array: List[float] = []
    HNZ_timely_availability_percentage_array: List[float] = []
    timely_availability_percentage_array_days_axis: List[date] = []
    for latency_dataframe in latencies:
        if not latency_dataframe.empty:
            HNN_latencies = latency_dataframe[latency_dataframe['channel'] ==
                                              "HNN"]
            total_number_of_HNN_latencies = HNN_latencies["data_latency"].size
            number_of_HNN_latencies_below_threshold =\
                HNN_latencies.loc[HNN_latencies["data_latency"]
                                  <= threshold]["data_latency"].size
            if total_number_of_HNN_latencies == 0:
                HNN_timely_availability_percentage_array.append(0.0)
            else:
                HNN_timely_availability_percentage_array.\
                    append(round(float(
                        number_of_HNN_latencies_below_threshold /
                        total_number_of_HNN_latencies * 100), 1))

            HNE_latencies = latency_dataframe[latency_dataframe['channel'] ==
                                              "HNE"]
            total_number_of_HNE_latencies = HNE_latencies["data_latency"].size
            number_of_HNE_latencies_below_threshold =\
                HNE_latencies.loc[HNE_latencies["data_latency"]
                                  <= threshold]["data_latency"].size
            if total_number_of_HNE_latencies == 0:
                HNE_timely_availability_percentage_array.append(0.0)
            else:
                HNE_timely_availability_percentage_array.\
                    append(round(float(
                        number_of_HNE_latencies_below_threshold /
                        total_number_of_HNE_latencies * 100), 1))

            HNZ_latencies = latency_dataframe[latency_dataframe['channel'] ==
                                              "HNZ"]
            total_number_of_HNZ_latencies = HNZ_latencies["data_latency"].size
            number_of_HNZ_latencies_below_threshold =\
                HNZ_latencies.loc[HNZ_latencies["data_latency"]
                                  <= threshold]["data_latency"].size

            if total_number_of_HNZ_latencies == 0:
                HNZ_timely_availability_percentage_array.append(0.0)
            else:
                HNZ_timely_availability_percentage_array.\
                    append(round(float(
                        number_of_HNZ_latencies_below_threshold /
                        total_number_of_HNZ_latencies * 100), 1))

            current_dataframe_date = arrow.get(
                latency_dataframe.iloc[0].startTime).format('YYYY-MM-DD')
            current_dataframe_date_dateobject = arrow.get(
                current_dataframe_date, 'YYYY-MM-DD').date()
            timely_availability_percentage_array_days_axis.append(
                current_dataframe_date_dateobject)

    return HNN_timely_availability_percentage_array, \
        HNE_timely_availability_percentage_array,\
        HNZ_timely_availability_percentage_array,\
        timely_availability_percentage_array_days_axis
