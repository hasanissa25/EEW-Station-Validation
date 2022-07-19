# flake8=noqa
import subprocess
from stationverification.utilities.get_latencies import get_latencies


def test_get_latencies(latency_parameters_nanometrics, latency_test_files_nanometrics, latency_parameters_guralp, latency_test_files_guralp):
    combined_latency_dataframe_for_all_days_dataframe,\
        array_of_daily_latency_objects_max_latency_only,\
        array_of_daily_latency_objects_all_latencies,\
        = get_latencies(
            typeofinstrument=latency_parameters_nanometrics.type_of_instrument,
            files=latency_test_files_nanometrics,
            network=latency_parameters_nanometrics.network,
            station=latency_parameters_nanometrics.station,
            startdate=latency_parameters_nanometrics.startdate,
            enddate=latency_parameters_nanometrics.enddate)
    assert len(array_of_daily_latency_objects_max_latency_only) == 3
    combined_latency_dataframe_for_all_days_dataframe,\
        array_of_daily_latency_objects_max_latency_only,\
        array_of_daily_latency_objects_all_latencies\
        = get_latencies(
            typeofinstrument=latency_parameters_guralp.type_of_instrument,
            files=latency_test_files_guralp,
            network=latency_parameters_guralp.network,
            station=latency_parameters_guralp.station,
            startdate=latency_parameters_guralp.startdate,
            enddate=latency_parameters_guralp.enddate)
    assert len(array_of_daily_latency_objects_max_latency_only) == 2
