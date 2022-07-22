import os

from datetime import date, timedelta
from typing import Optional

from pandas.core.frame import DataFrame


def generate_CSV_from_failed_latencies(latencies: DataFrame,
                                       station: str,
                                       network: str,
                                       startdate: date,
                                       enddate: date,
                                       timely_threshold: float,
                                       location: Optional[str] = None,
                                       ):
    if location is None:
        snlc = f'{network}.{station}..'
    else:
        snlc = f'{network}.{station}.{location}.'
    if startdate == enddate - timedelta(days=1):
        filename = f'{snlc}.{startdate}'
    else:
        filename = f'{snlc}.{startdate}_\
{enddate - timedelta(days=1)}'
    latencies_above_three = latencies.loc[latencies.data_latency
                                          > timely_threshold]
    # This part is specifically for Guralp Latencies.
    # Need to look into if its neccessary
    # if 'date' in latencies.columns:
    #     latencies.drop(
    #         'date', axis=1, inplace=True)
    latencies_above_three_rounded = latencies_above_three.loc[:,
                                                              ['network',
                                                               'station',
                                                               'channel',
                                                               'startTime',
                                                               'data_latency']]

    latencies_above_three_rounded["data_latency"] = round(
        latencies_above_three_rounded.data_latency.astype(float), 1)

    if not os.path.isdir('./stationvalidation_output/'):
        os.mkdir('./stationvalidation_output/')
    latencies_above_three_rounded.to_csv(
        f'./stationvalidation_output/{filename}.failed_latencies.csv',
        index=False)
    latencies.to_csv(
        f'./stationvalidation_output/{filename}.all_latencies.csv',
        index=False)
