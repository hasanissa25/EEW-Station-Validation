'''
Python script used to check the quality of data coming from new EEW Stations
in order to validate that the stations are suitable for production.

usage: stationverification [-h] -N NETWORK -S STATION -d STARTDATE -e ENDDATE
                           -s STATIONURL -m MINISEEDARCHIVE -l LATENCYARCHIVE
                           -H SOHARCHIVE -i ISPAQLOCATION -T TYPEOFINSTRUMENT

Functions:
----------
main()
    The main fuction, which takes care of calling the other functions and
    running ISPAQ
'''
import logging
from multiprocessing import Process, Queue
from datetime import timedelta
from typing import Any
from stationverification.utilities.cleanup_directory import cleanup_directory
from stationverification.utilities.fetch_arguments import fetch_arguments
from stationverification.utilities.generate_latency_results import \
    generate_latency_results
from stationverification.utilities.generate_plots import (PlotParameters,
                                                          plot_metrics)
from stationverification.utilities.generate_report import gather_stats, report
from stationverification.utilities.handle_running_ispaq_command import \
    handle_running_ispaq_command
from stationverification.utilities.upload_results_to_s3 import \
    upload_results_to_s3
from stationverification.utilities.timely_availability_plot import \
    timely_availability_plot
from stationverification.utilities.update_station_xml import update_station_xml
from stationverification.utilities.fetch_arguments import UserInput


def main():
    '''
    The Main function.

    Returns
    -------
    {station}_results.json
        A json file containing the results of the stationvalidation tests.

    '''
    user_inputs = fetch_arguments()

    if user_inputs.updateStationXml:
        # Fetching the updated station xml for QW network
        update_station_xml()
    if user_inputs.psdOnly is True:
        psd_plots_only(user_inputs=user_inputs)
    else:
        latency_and_ispq_metrics(user_inputs=user_inputs)


def latency_and_ispq_metrics(user_inputs: UserInput):
    # Setting up a queue for processors to push their results to if needed
    queue: Any = Queue()  # noqa

    # Run Latency
    logging.info("Process 1: Generating Latency results..")
    process_one = Process(
        target=generate_latency_results, args=(user_inputs.typeofinstrument,
                                               user_inputs.network,
                                               user_inputs.station,
                                               user_inputs.startdate,
                                               user_inputs.enddate,
                                               user_inputs.latencyFiles,
                                               user_inputs.thresholds
                                               .getfloat('thresholds',
                                                         'data_timeliness',
                                                         fallback=3),
                                               user_inputs.location,
                                               queue,
                                               ))
    process_one.start()
    # Run ISPAQ
    logging.info("Process 2: Generating ISPAQ results..")
    process_two = Process(
        target=handle_running_ispaq_command, args=(
            user_inputs.ispaqloc,
            user_inputs.metrics,
            user_inputs.startdate,
            user_inputs.enddate,
            user_inputs.pfile,
            user_inputs.pdfinterval,
            user_inputs.miniseedarchive,
            user_inputs.network,
            user_inputs.station,
            user_inputs.location,
            user_inputs.station_url,
            # user_inputs.stationconf,
        ))
    process_two.start()
    latency_results = queue.get()
    combined_latency_dataframe_for_all_days,\
        array_of_daily_latency_dataframes_all_latencies = latency_results
    process_one.join()
    logging.info("Finished Process 1: Generating Latency results")
    process_two.join()
    logging.info("Finished Process 2: Generating ISPAQ results")

    # Read the files generated from ISPAQ and populate the dictionary object
    if user_inputs.location is None:
        snlc = f'{user_inputs.network}.{user_inputs.station}.x.Hxx'
    else:
        snlc = f'{user_inputs.network}.\
{user_inputs.station}.{user_inputs.location}.Hxx'

    stationMetricData = gather_stats(
        snlc=snlc,
        start=user_inputs.startdate,
        stop=user_inputs.enddate,
        metrics=user_inputs.metrics)

    for channel in stationMetricData.get_channels(
        network=user_inputs.network,
        station=user_inputs.station
    ):
        plot_metrics(
            PlotParameters(network=user_inputs.network,
                           station=user_inputs.station,
                           location=user_inputs.location,
                           channel=channel,
                           stationMetricData=stationMetricData,
                           start=user_inputs.startdate,
                           stop=user_inputs.enddate)
        )
    logging.info("Generating timely availability plot..")
    timely_availability_plot(
        latencies=array_of_daily_latency_dataframes_all_latencies,
        stationMetricData=stationMetricData,
        station=user_inputs.station,
        startdate=user_inputs.startdate,
        enddate=user_inputs.enddate,
        network=user_inputs.network,
        timely_threshold=user_inputs.thresholds
        .getfloat('thresholds',
                  'data_timeliness',
                  fallback=3),
        location=user_inputs.location
    )
    logging.info("Generating report..")

    report(
        combined_latency_dataframe_for_all_days=combined_latency_dataframe_for_all_days,  # noqa
        typeofinstrument=user_inputs.typeofinstrument,
        network=user_inputs.network,
        station=user_inputs.station,
        location=user_inputs.location,
        stationmetricdata=stationMetricData,
        start=user_inputs.startdate,
        end=user_inputs.enddate,
        thresholds=user_inputs.thresholds,
        soharchive=user_inputs.soharchive,
        miniseed_directory=user_inputs.miniseedarchive,
        timingSource=user_inputs.timingSource

    )

    # Delete temporary files and links and package the output in a tarball
    logging.info("Cleaning up directory..")
    cleanup_directory(
        network=user_inputs.network,
        station=user_inputs.station,
        startdate=user_inputs.startdate,
        enddate=user_inputs.enddate,
        outputdir=user_inputs.outputdir,
        instrumentGain=user_inputs.instrument_gain)

    if user_inputs.uploadresultstos3 is True:
        if user_inputs.startdate == user_inputs.enddate - timedelta(days=1):
            validation_output_directory = f'{user_inputs.outputdir}/{user_inputs.network}/{user_inputs.station}/\
    {user_inputs.startdate}'
        else:
            validation_output_directory = f'{user_inputs.outputdir}/{user_inputs.network}/{user_inputs.station}/\
    {user_inputs.startdate}-{user_inputs.enddate}'

        upload_results_to_s3(path_of_folder_to_upload=validation_output_directory,  # noqa
                             bucketName=user_inputs.bucketName,
                             s3directory=user_inputs.s3directory)


def psd_plots_only(user_inputs: UserInput):
    logging.info("Generating ISPAQ results")
    handle_running_ispaq_command(
        ispaqloc=user_inputs.ispaqloc,
        metrics="eew_only_psd",
        startdate=user_inputs.startdate,
        enddate=user_inputs.enddate,
        pfile=user_inputs.pfile,
        pdfinterval=user_inputs.pdfinterval,
        miniseedarchive=user_inputs.miniseedarchive,
        network=user_inputs.network,
        station=user_inputs.station,
        location=user_inputs.location,
        station_url=user_inputs.station_url
    )

    logging.info("Cleaning up directory..")
    cleanup_directory(
        network=user_inputs.network,
        station=user_inputs.station,
        startdate=user_inputs.startdate,
        enddate=user_inputs.enddate,
        outputdir=user_inputs.outputdir,
        instrumentGain=user_inputs.instrument_gain)
