'''
Python script used to produce latency plots for the given period.

usage: stationverificationlatency [-h] -T instrumentType -N NETWORK -S STATION\
     -d STARTDATE -e ENDDATE -l LatencyDirectory

optional arguments:
    -h, --help            show this help message and exit
    -N network, --network NETWORK
                        The station's unique network code. Ex. QW
    -S STATION, --station STATION
                        The station's unique code. Ex. QCC001
    -d STARTDATE, --startdate STARTDATE
                        The first date of the verification period. Must be in
                        YYYY-MM-DD format
    -e ENDDATE, --enddate ENDDATE
                        The end of the verification period. Data will be
                        tested for each day from the start date up to but not
                        including the end date. Must be in YYYY-MM-DD format.
    -t THRESHOLDS, --thresholds THRESHOLDS
                        The path to the preference file containing the
                        thresholds to test the metrics against.
    -l LatencyDirectory, --latency LatencyDirectory
                        The directory containing latency files
    -U UPLOADTOS3, --uploadresultstos3 UPLOADTOS3
                        Whether or not to upload results to the S3 bucket.\
 True or False
    -b NAMEOFS3BUCKET, --s3bucketname NAMEOFS3BUCKET
                        To which bucket to upload in S3
    -B S3PATHTOSAVETO, --s3bucketpathtosaveto S3PATHTOSAVETO
                        Which 'directory' in S3 to save to
Functions:
----------
main()
    The main fuction, which takes care of calling the other functions
'''
import logging

from datetime import timedelta
from stationverification.utilities.cleanup_directory \
    import cleanup_directory_after_latency_call, initialize_directory

from stationverification.utilities.fetch_arguments import fetch_arguments
from stationverification.utilities.generate_latency_results \
    import generate_latency_results
from stationverification.utilities.upload_results_to_s3 import \
    upload_results_to_s3
from stationverification.utilities.update_station_xml import update_station_xml


def main():
    '''
    The Main function.

    Returns
    -------
        JSON file containing the results of the stationvalidation tests,
        Latency line plot for each day of the validation period
        Latency log plot for the validation period
        CSV file of failed latencies
        A Timely Availability Plot of the validation period

    '''

    # Fetching the updated station xml for QW network
    initialize_directory()
    update_station_xml()
    user_inputs = fetch_arguments()

    generate_latency_results(typeofinstrument=user_inputs.typeofinstrument,
                             network=user_inputs.network,
                             station=user_inputs.station,
                             startdate=user_inputs.startdate,
                             enddate=user_inputs.enddate,
                             path=user_inputs.latencyFiles,
                             timely_threshold=user_inputs.thresholds
                             .getfloat(
                                 'thresholds', 'data_timeliness',
                                 fallback=3))
    logging.info("Cleaning up directory..")

    cleanup_directory_after_latency_call(startdate=user_inputs.startdate,
                                         enddate=user_inputs.enddate,
                                         network=user_inputs.network,
                                         station=user_inputs.station,
                                         outputdir=user_inputs.outputdir)
    if user_inputs.uploadresultstos3 is True:
        logging.info("Uploading to S3 bucket..")
        if user_inputs.startdate == user_inputs.enddate - timedelta(days=1):
            validation_output_directory = f'{user_inputs.outputdir}/{user_inputs.network}/{user_inputs.station}/\
{user_inputs.startdate}'
        else:
            validation_output_directory = f'{user_inputs.outputdir}/{user_inputs.network}/{user_inputs.station}/\
{user_inputs.startdate}-{user_inputs.enddate}'
        upload_results_to_s3(path_of_folder_to_upload=validation_output_directory,  # noqa
                             bucketName=user_inputs.bucketName,
                             s3directory=user_inputs.s3directory)
