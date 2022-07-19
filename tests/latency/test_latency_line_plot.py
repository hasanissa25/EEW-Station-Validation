# flake8:noqa
import subprocess
from pathlib import Path

from stationverification.utilities.latency_line_plot import latency_line_plot
from stationverification.utilities.get_latencies import get_latencies
from stationverification.utilities.\
    convert_array_of_latency_objects_into_array_of_dataframes \
    import convert_array_of_latency_objects_into_array_of_dataframes


def test_latency_line_plot(latency_parameters_nanometrics, latency_test_files_nanometrics):
    subprocess.getoutput(
        "rm -rf 'stationvalidation_output'")
    combined_latency_dataframe_for_all_days_dataframe,\
        array_of_daily_latency_objects_max_latency_only,\
        array_of_daily_latency_objects_all_latencies = get_latencies(
            typeofinstrument=latency_parameters_nanometrics.type_of_instrument,
            files=latency_test_files_nanometrics,
            network=latency_parameters_nanometrics.network,
            station=latency_parameters_nanometrics.station,
            startdate=latency_parameters_nanometrics.startdate,
            enddate=latency_parameters_nanometrics.enddate)
    array_of_daily_latency_dataframes = \
        convert_array_of_latency_objects_into_array_of_dataframes(
            array_of_latencies=array_of_daily_latency_objects_max_latency_only)
    latency_line_plot(latencies=array_of_daily_latency_dataframes,
                      station=latency_parameters_nanometrics.station,
                      network=latency_parameters_nanometrics.network,
                      timely_threshold=latency_parameters_nanometrics.timely_threshold
                      )
    latency_line_plot_1 = Path(
        "stationvalidation_output/QW.QCC02...2022-04-01.latency_line_plot.png")
    if latency_line_plot_1.exists():
        assert True
    else:
        assert False
    latency_line_plot_2 = Path(
        "stationvalidation_output/QW.QCC02...2022-04-02.latency_line_plot.png")
    if latency_line_plot_2.exists():
        assert True
    else:
        assert False
    latency_line_plot_3 = Path(
        "stationvalidation_output/QW.QCC02...2022-04-03.latency_line_plot.png")
    if latency_line_plot_3.exists():
        assert True
    else:
        assert False
    subprocess.getoutput(
        "rm -rf 'stationvalidation_output'")
