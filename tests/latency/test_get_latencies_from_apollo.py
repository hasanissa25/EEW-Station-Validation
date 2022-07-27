# flake8=noqa
import subprocess
import pytest
from stationverification.utilities.get_latencies_from_apollo import get_latencies_from_apollo
from stationverification.utilities import exceptions
import numpy as np
import logging


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

    ar = np.array(combined_latency_dataframe_for_all_days_dataframe)
    br = np.array([
        3.5, 1.5, 2.0, 2.0, 6.0, 2.0, 3.0, 3.0, 4.5, 2.6, 3.0, 3.0, 3.0])
    assert ar.all() == br.all()
    with pytest.raises(exceptions.LatencyFileError):
        get_latencies_from_apollo(
            files=latency_test_file_nanometrics_bad_file,
            network=latency_parameters_nanometrics.network,
            station=latency_parameters_nanometrics.station)
