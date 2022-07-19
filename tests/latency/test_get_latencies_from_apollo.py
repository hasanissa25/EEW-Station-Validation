# flake8=noqa
import subprocess
import pytest
from stationverification.utilities.get_latencies_from_apollo import get_latencies_from_apollo
from stationverification.utilities import exceptions


def test_get_latencies_from_apollo(latency_parameters_nanometrics,
                                   latency_test_file_nanometrics_over_3_packets,
                                   latency_test_file_nanometrics_bad_file):
    subprocess.getoutput(
        "rm -rf 'stationvalidation_output'")
    combined_latency_dataframe_for_all_days_dataframe, \
        array_of_daily_latency_objects_max_latency_only,\
        array_of_daily_latency_objects_all_latencies = get_latencies_from_apollo(
            files=latency_test_file_nanometrics_over_3_packets,
            network=latency_parameters_nanometrics.network,
            station=latency_parameters_nanometrics.station)

    assert combined_latency_dataframe_for_all_days_dataframe.loc[
        "QW.QCC02.HNE.2022-04-03T00:00:00.000000000Z.max"].data_latency == 3.5
    assert combined_latency_dataframe_for_all_days_dataframe.loc[
        "QW.QCC02.HNZ.2022-04-03T00:00:00.000000000Z.min"].data_latency == 2.6
    with pytest.raises(exceptions.LatencyFileError):
        get_latencies_from_apollo(
            files=latency_test_file_nanometrics_bad_file,
            network=latency_parameters_nanometrics.network,
            station=latency_parameters_nanometrics.station)
