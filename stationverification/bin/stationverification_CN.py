'''
Python script used to check the quality of data coming from new EEW Stations
in order to validate that the stations are suitable for production.

usage: stationverification [-h] -N NETWORK -S STATION -d STARTDATE -e ENDDATE
                           -s STATIONURL -m MINISEEDARCHIVE -l LATENCYARCHIVE
                           -H SOHARCHIVE -i ISPAQLOCATION -T TYPEOFINSTRUMENT

optional arguments:
    -h, --help            show this help message and exit
    -N NETWORK, --network NETWORK
                        The networks unique code. Ex. QW
    -S STATION, --station STATION
                        The station's unique code. Ex. QCQ
    -d STARTDATE, --startdate STARTDATE
                        The first date of the verification period. Must be in
                        YYYY-M-D format
    -e ENDDATE, --enddate ENDDATE
                        The end of the verification period. Data will be
                        tested for each day from the start date up to but not
                        including the end date. Must be in YYYY-MM-DD format.
    -i ISPAQLOCATION, --ispaqlocation ISPAQLOCATION
                        If ispaq is not installed as a package, specify the
                        location of run_ispaq.py

    -m miniseedDirectory, --miniseedarchive miniseedDirectory
                        The directory containing miniseed files
    -s station_url, --station_url station_url
                        FDSN webservice or path to stationXML



Functions:
----------
main()
    The main fuction, which takes care of calling the other functions and
    running ISPAQ
'''
import logging
from multiprocessing import Process
from stationverification.utilities.cleanup_directory import cleanup_directory
from stationverification.utilities.fetch_arguments_CN import fetch_arguments_CN

from stationverification.utilities.generate_plots import (PlotParameters,
                                                          plot_metrics)
from stationverification.utilities.generate_report import gather_stats
from stationverification.utilities.handle_running_ispaq_command_CN import \
    handle_running_ispaq_command_CN

logging.basicConfig(
    format='%(asctime)s Station Validation: %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def main():
    '''
    The Main function.

    Returns
    -------
    {station}_results.json
        A json file containing the results of the stationvalidation tests.

    '''
    user_inputs = fetch_arguments_CN()

    # Run ISPAQ
    logging.info("Process 1: Generating ISPAQ results..")
    process_one = Process(
        target=handle_running_ispaq_command_CN, args=(
            user_inputs.ispaqloc,
            user_inputs.metrics,
            user_inputs.startdate,
            user_inputs.enddate,
            user_inputs.pfile,
            user_inputs.pdfinterval,
            user_inputs.miniseedarchive,
            user_inputs.network,
            user_inputs.station,
        ))
    process_one.start()
    process_one.join()
    logging.info("Finished Process 1: Generating ISPAQ results")

    # Read the files generated from ISPAQ and populate the dictionary object
    if user_inputs.location is None:
        snlc = f'{user_inputs.network}.{user_inputs.station}.x.xxx'
    else:
        snlc = f'{user_inputs.network}.\
{user_inputs.station}.{user_inputs.location}.xxx'

    stationMetricData = gather_stats(
        snlc=snlc,
        start=user_inputs.startdate,
        stop=user_inputs.enddate,
        metrics=user_inputs.metrics)
    logging.info("Plotting metrics..")

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

    # Delete temporary files and links and package the output in a tarball
    logging.info("Cleaning up directory..")
    cleanup_directory(
        network=user_inputs.network,
        station=user_inputs.station,
        startdate=user_inputs.startdate,
        enddate=user_inputs.enddate,
        outputdir=user_inputs.outputdir)
