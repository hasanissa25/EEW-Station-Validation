from pandas.core.frame import DataFrame
from datetime import date
import os


def generate_CSV_from_failed_latencies(latencies: DataFrame,
                                       station: str,
                                       network: str,
                                       startdate: date,
                                       enddate: date):
    filename = f'{network}.{station}-{startdate}_to_{enddate}-failed_latencies.csv'
    latencies_above_three = latencies[latencies["data_latency"] > 3]
    if not os.path.isdir("./station_validation_results"):
        os.mkdir('./station_validation_results')
    latencies_above_three.to_csv(
        f'station_validation_results/{filename}', index=False)
