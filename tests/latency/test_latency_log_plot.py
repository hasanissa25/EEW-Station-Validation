# flake8:noqa
import subprocess
from datetime import date
from pathlib import Path
from stationverification.utilities.calculate_total_availability_for_nanometrics import calculate_total_availability_for_nanometrics

from stationverification.utilities.latency_log_plot import latency_log_plot
from stationverification.utilities.get_latencies import get_latencies


def test_latency_log_plot(latency_parameters_nanometrics,
                          latency_test_files_nanometrics,
                          latency_test_file_nanometrics_over_3_packets,
                          latency_parameters_guralp,
                          latency_test_files_guralp):
    subprocess.getoutput(
        "rm -rf 'stationvalidation_output'")
    # Multiple days, Nanometric data
    total_availability = calculate_total_availability_for_nanometrics(
        latency_test_files_nanometrics)
    combined_latency_dataframe_for_all_days_dataframe,\
        array_of_daily_latency_objects_max_latency_only,\
        array_of_daily_latency_objects_all_latencies = get_latencies(
            typeofinstrument=latency_parameters_nanometrics.type_of_instrument,
            files=latency_test_files_nanometrics,
            network=latency_parameters_nanometrics.network,
            station=latency_parameters_nanometrics.station,
            startdate=latency_parameters_nanometrics.startdate,
            enddate=latency_parameters_nanometrics.enddate)
    latency_log_plot(latencies=combined_latency_dataframe_for_all_days_dataframe,
                     typeofinstrument=latency_parameters_nanometrics.type_of_instrument,
                     startdate=latency_parameters_nanometrics.startdate,
                     enddate=latency_parameters_nanometrics.enddate,
                     network=latency_parameters_nanometrics.network,
                     station=latency_parameters_nanometrics.station,
                     timely_threshold=latency_parameters_nanometrics.timely_threshold,
                     total_availability=total_availability
                     )
    # 1 day, Nanometric data
    total_availability = calculate_total_availability_for_nanometrics(
        latency_test_file_nanometrics_over_3_packets)
    combined_latency_dataframe_for_all_days_dataframe,\
        array_of_daily_latency_objects_max_latency_only,\
        array_of_daily_latency_objects_all_latencies = get_latencies(
            typeofinstrument=latency_parameters_nanometrics.type_of_instrument,
            files=latency_test_file_nanometrics_over_3_packets,
            network=latency_parameters_nanometrics.network,
            station=latency_parameters_nanometrics.station,
            startdate=date(2022, 4, 3),
            enddate=date(2022, 4, 4))
    latency_log_plot(latencies=combined_latency_dataframe_for_all_days_dataframe,
                     typeofinstrument=latency_parameters_nanometrics.type_of_instrument,
                     startdate=date(2022, 4, 3),
                     enddate=date(2022, 4, 4),
                     network=latency_parameters_nanometrics.network,
                     station=latency_parameters_nanometrics.station,
                     timely_threshold=latency_parameters_nanometrics.timely_threshold,
                     total_availability=total_availability
                     )
    # Multiple days, Guralp data
    combined_latency_dataframe_for_all_days_dataframe,\
        array_of_daily_latency_objects_max_latency_only,\
        array_of_daily_latency_objects_all_latencies = get_latencies(
            typeofinstrument=latency_parameters_guralp.type_of_instrument,
            files=latency_test_files_guralp,
            network=latency_parameters_guralp.network,
            station=latency_parameters_guralp.station,
            startdate=latency_parameters_guralp.startdate,
            enddate=latency_parameters_guralp.enddate)
    latency_log_plot(latencies=combined_latency_dataframe_for_all_days_dataframe,
                     typeofinstrument=latency_parameters_guralp.type_of_instrument,
                     startdate=latency_parameters_guralp.startdate,
                     enddate=latency_parameters_guralp.enddate,
                     network=latency_parameters_guralp.network,
                     station=latency_parameters_guralp.station,
                     timely_threshold=latency_parameters_guralp.timely_threshold,
                     )
    test_latency_log_plot_Nanometrics_1 = Path(
        "stationvalidation_output/QW.QCC02...2022-04-01_2022-04-03.latency_log_plot.png")
    if test_latency_log_plot_Nanometrics_1.exists():
        assert True
    else:
        assert False
    test_latency_log_plot_Nanometrics_2 = Path(
        "stationvalidation_output/QW.QCC02...2022-04-03.latency_log_plot.png")
    if test_latency_log_plot_Nanometrics_2.exists():
        assert True
    else:
        assert False
    test_latency_log_plot_Guralp = Path(
        "stationvalidation_output/QW.QCN08...2022-03-01_2022-03-02.latency_log_plot.png")
    if test_latency_log_plot_Guralp.exists():
        assert True
    else:
        assert False
    subprocess.getoutput(
        "rm -rf 'stationvalidation_output'")
