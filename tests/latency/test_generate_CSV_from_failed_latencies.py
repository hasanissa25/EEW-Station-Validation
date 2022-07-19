# flake8:noqa
import subprocess
from stationverification.utilities.generate_CSV_from_failed_latencies import generate_CSV_from_failed_latencies
from pathlib import Path


def test_generate_CSV_from_failed_latencies(latency_parameters_nanometrics, latency_dataframe):
    combined_latency_dataframe_for_all_days = latency_dataframe
    subprocess.getoutput(
        "rm -rf 'stationvalidation_output'")
    generate_CSV_from_failed_latencies(latencies=combined_latency_dataframe_for_all_days,
                                       station=latency_parameters_nanometrics.station,
                                       network=latency_parameters_nanometrics.network,
                                       startdate=latency_parameters_nanometrics.startdate,
                                       enddate=latency_parameters_nanometrics.enddate,
                                       timely_threshold=latency_parameters_nanometrics.timely_threshold)
    file_name = Path(
        "stationvalidation_output/QW.QCC02...2022-04-01_2022-04-03.failed_latencies.csv")
    if file_name.exists():
        with open('stationvalidation_output/QW.QCC02...2022-04-01_2022-04-03.failed_latencies.csv') as failed_latencies:
            contents = failed_latencies.read()
            assert contents == 'network,station,channel,startTime,data_latency\nQW,QCC02,HNZ,2022-04-01,5.0\nQW,QCC02,HNZ,2022-04-02,4.0\n'
        subprocess.getoutput(
            "rm 'stationvalidation_output/QW.QCC02...2022-04-01_2022-04-03.failed_latencies.csv'")
    else:
        assert False
