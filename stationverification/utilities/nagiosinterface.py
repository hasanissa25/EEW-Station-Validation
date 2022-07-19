# '''
# This module contains functions used to push report results to Nagios to
# populate services

# Functions
# ---------

# list_reports
#     Gets a list of all files in a specified directory

# check_report_metrics
#     Gathers latency statistics and select metrics from a verification report
#     json and formats them to be sent to Nagios nrpd to be used as Service
#     Checks.

# latency_check
#     Gather the latency statistics from a verification report and package them
#     to be sent to Nagios

# metric_check
#     Function to package the results for a specific ispaq method to be sent to
#     Nagios
# '''
# from os import listdir
# from os.path import join
# import json
# from stationverification import nagios
# from stationverification.nagios import nrdp
# import logging

# flake8: noqa

# def list_reports(
#     path: str
# ) -> list:
#     '''
#     Given a directory, returns a list of files contained within

#     Parameters
#     ----------
#     path: string
#         The path to the directory to search for files.

#     Returns
#     -------
#     list
#         List of file paths

#     Raises
#     ------
#     FileNotFoundError
#         When no files are located in the specified directory.
#     '''

#     # Obtain a list of the contents of the directory
#     files = listdir(path)

#     # Raise an exception if no files are found
#     if len(files) <= 0:
#         raise FileNotFoundError(f'No files found in {path}')

#     # Loop through the list of files and convert them to their path
#     for file in files:
#         files[files.index(file)] = join(path, file)

#     return files


# def check_report_metrics(
#     file: str,
#     metrics: list
# ) -> nrdp.NagiosCheckResults:
#     '''
#     Parses a verification report json file and assembles the results in a
#     NagiosCheckResults object.

#     Parameters
#     ----------
#     file: string
#         The path to the json verification report to parse

#     metrics: list
#         List of ispaq metrics to gather results for

#     Returns
#     -------
#     NagiosCheckResults
#         Object containing information to send to Nagios nrdp API
#     '''
#     checkresults = nrdp.NagiosCheckResults()
#     # Open the report file and load it into a dictionary object.
#     try:
#         with open(file, 'r') as f:
#             report = json.load(f)
#     # Skip file if it's not in json format
#     except UnicodeDecodeError:
#         logging.warning(f'{file} not valid json, skipping.')
#         return checkresults

#     # Assemble the hostname
#     try:
#         network = report['network_code']
#         station = report['station_code']
#     except KeyError as e:
#         # If the network or station codes aren't in the json file, skip it
#         logging.warning(f'{e} missing from {file}, skipping')
#         return checkresults
#     hostname = f'{network}-{station}-digitizer'

#     # Add latency results to be sent to nagios
#     checkresults.append(latency_check(hostname, report))

#     # Add results for the specified ispaq metrics
#     for metric in metrics:
#         metric = metric.strip(' ')
#         checkresults.append(metric_check(hostname, report, metric))

#     return checkresults


# def latency_check(
#     hostname: str,
#     report: dict
# ) -> nrdp.NagiosCheckResult:
#     '''
#     Gather the latency statistics from a verification report and package them
#     to be sent to Nagios

#     Parameters
#     ----------
#     hostname: string
#         The nagios hostname for the subject of the report

#     report: dictionary
#         Json format dictionary containing the results of a verification report

#     Returns
#     -------
#     NagiosCheckResult
#         Results formatted to be sent to Nagios
#     '''

#     # Setup the structure of the message
#     message = '{state} - {id} = {value} | {performance}'

#     # Get average latency for the station from the report
#     try:
#         avglat = report['latency']['average_latency']
#     except KeyError:
#         # If for some reason latency information isn't in the report, skip it
#         logging.warning(f'Skipping latency for {hostname}')
#         return
#     # Set the nagios state based on whether the latency received a passing
#     # grade
#     state = nagios.STATE_OK
#     statetxt = 'OK'
#     if not report['latency']['timely_passed']:
#         state = nagios.STATE_WARNING
#         statetxt = 'WARNING'

#     # Assemble performance statistics with average and average per channel
#     # statistics
#     performance = 'avg=%.2f;' % avglat
#     for channel in report['channels']:
#         lat = report['channels'][channel]['latency']['average_latency']
#         performance += ('%s=%.2f;' % (channel, lat))
#     # Trim off the last semicolon
#     performance = performance.rstrip(';')

#     # Assemble the message to send to Nagios
#     content = message.format(
#         state=statetxt,
#         id=hostname,
#         value=avglat,
#         performance=performance
#     )

#     # Format results to be sent to Nagios
#     return nrdp.NagiosCheckResult(
#         hostname=hostname,
#         servicename='Yesterdays Average Latency',
#         state=state,
#         output=content)


# def metric_check(
#     hostname: str,
#     report: dict,
#     metric: str
# ) -> nrdp.NagiosCheckResult:
#     '''
#     Function to package the results for a specific ispaq method to be sent to
#     Nagios

#     Parameters
#     ----------

#     hostname: string
#         The Nagios hostname for the subject of the report

#     report: dictionary
#         Report results in json format dictionary

#     metric: string
#         The name of the metric to check as it appears in the report and in
#         ispaq

#     Returns
#     -------
#     NagiosCheckResult
#         An object containing the check results for a single Nagios check
#     '''

#     # Define the structure of the message to send to Nagios
#     message = '{state} - {id} = {value} | {performance}'

#     # Initialize variables
#     state = nagios.STATE_OK
#     statetxt = 'OK'
#     performance = ''
#     values = []

#     # Loop through each channel in the report
#     for channel in report['channels']:
#         try:
#             num = report['channels'][channel]['metrics'][metric]['values']
#         except KeyError:
#             # If the metric isn't found under a specific channel, skip.
#             logging.warning(
#                 f'Metric {metric} missing for channel {channel}, skipping.')
#             continue
#         values += num
#         # Flag the state as warning if the metric received a fail for any
#         # channel
#         if not report['channels'][channel]['metrics'][metric]['passed']:
#             state = nagios.STATE_WARNING
#             statetxt = 'WARNING'
#         # Concatonate the channel's metric results to the performance string
#         performance += ('%s=%.2f;' % (channel, num[0]))

#     if len(values) < 1:
#         logging.warning(f'No results for {metric} found for {hostname}')
#         return
#     # Strip off the last semicolon
#     performance = performance.rstrip(';')

#     # Calculate the average between all channels
#     avg = sum(values)/len(values)
#     content = message.format(
#         state=statetxt,
#         id=hostname,
#         value=avg,
#         performance=performance)

#     # Return results in format to be sent to Nagios
#     return nrdp.NagiosCheckResult(
#         hostname=hostname,
#         servicename=f'Yesterdays {metric}',
#         state=state,
#         output=content)
