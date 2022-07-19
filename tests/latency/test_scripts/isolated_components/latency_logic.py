# type: ignore
# flake8: noqa

# This script is to test our latency generating logic, from fetching the files, to producing the plots
import os
import json
import logging

from datetime import date

from stationverification.utilities.calculate_total_availability_for_nanometrics import calculate_total_availability_for_nanometrics
from stationverification.utilities.latency import get_latency_files, latency_log_plot, latency_line_plot, generate_CSV_from_failed_latencies, populate_json_with_latency_info
from stationverification.utilities.timely_availability_plot import timely_availability_plot
from stationverification.utilities.get_latencies import get_latencies

# from tests.latency.test_scripts.isolated_components.latency_line_plot_test import latency_line_plot_test
# Apollo Parameters
required_network = "QW"
required_station = "QCC02"
typeofinstrument = 'APOLLO'
path = 'tests/data/apollo/archive/latency'
startdate = date(2022, 4, 4)
enddate = date(2022, 4, 5)
timely_threshold = 3
json_dict = {
    "channels": {
        "HNN": {},
        "HNE": {},
        "HNZ": {}
    }}
# Guralp Parameters
# required_network = "QW"
# required_station = "QCN08"
# typeofinstrument = 'GURALP'
# path = 'tests/data/guralp/archive/latency'
# startdate = date(2022, 3, 17)
# enddate = date(2022, 3, 23)

# Returns the file paths containing the latencies in the validation period for the required network and station
files = get_latency_files(typeofinstrument=typeofinstrument,
                          network=required_network,
                          station=required_station,
                          path=path,
                          startdate=startdate,
                          enddate=enddate)
# Returns the latency handling both Guralp and Apollo
logging.info(f"Getting latencies")
combined_latency_dataframe_for_all_days_dataframe, array_of_daily_latency_dataframes = get_latencies(
    typeofinstrument=typeofinstrument,
    files=files,
    network=required_network,
    station=required_station,
    startdate=startdate,
    enddate=enddate)

# logging.info(
#     f"array_of_daily_latency_dataframes \n {array_of_daily_latency_dataframes}")
# total_availability = calculate_total_availability_for_nanometrics(files)
# generate_CSV_from_failed_latencies(latencies=combined_latency_dataframe_for_all_days_dataframe,
#                                    station=required_station,
#                                    network=required_network,
#                                    startdate=startdate,
#                                    enddate=enddate,
#                                    timely_threshold=timely_threshold)

# timely_availability_plot(latencies=array_of_daily_latency_dataframes,
#                          station=required_station,
#                          startdate=startdate,
#                          enddate=enddate,
#                          network=required_network,
#                          timely_threshold=timely_threshold
#                          )

# latency_log_plot(latencies=combined_latency_dataframe_for_all_days_dataframe,
#                  station=required_station,
#                  startdate=startdate,
#                  enddate=enddate,
#                  typeofinstrument=typeofinstrument,
#                  network=required_network,
#                  timely_threshold=timely_threshold,
#                  total_availability=total_availability
#                  )

# logging.info("Producing Latency Line Plot")
# latency_line_plot(latencies=array_of_daily_latency_dataframes,
#                   network=required_network,
#                   station=required_station,
#                   startdate=startdate,
#                   timely_threshold=timely_threshold
#                   )
# logging.info("Latency Line Plot produced")

# json_of_latency = populate_json_with_latency_info(
#     json_dict=json_dict,
#     combined_latency_dataframe_for_all_days_dataframe=combined_latency_dataframe_for_all_days_dataframe,
#     network=required_network,
#     station=required_station,
#     timely_threshold=3,
#     timely_percent=97
# )

# if not os.path.isdir('./station_validation_results/'):
#     os.mkdir('./station_validation_results/')
# with open('./station_validation_results/json_report.json', 'w+') as file:
#     json.dump(json_dict, file, indent=2)
