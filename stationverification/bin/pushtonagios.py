# '''
# This cmdline tool pushes daily ispaq results to Nagios.
# '''
# import argparse
# from stationverification.nagios import nrdp
# from stationverification.utilities.nagiosinterface import check_report_metrics
# from stationverification.utilities.nagiosinterface import list_reports
# from datetime import datetime, timedelta
# from stationverification import CONFIG
# from configparser import ConfigParser
# import logging

# flake8: noqa

# def main():
#     '''
#     Main function. Locates daily report for yesterday and pushes it to Nagios.
#     '''
#     argsparser = argparse.ArgumentParser()
#     argsparser.add_argument(
#         '-a',
#         '--archivepath',
#         help='The path to the archived verification report',
#         type=str,
#         default='./dailyverification'
#     )
#     argsparser.add_argument(
#         '-n',
#         '--nagiosurl',
#         help='Overrides the default URL for the Nagios nrdp server to push \
# results to. Defaults are stored in config.ini',
#         type=str,
#         default=None
#     ),
#     argsparser.add_argument(
#         '-t',
#         '--token',
#         help='Overrides the Nagios API token in config.ini.',
#         type=str,
#         default=None
#     )
#     argsparser.add_argument(
#         '-c',
#         '--nagios_config',
#         help='Override the default config file.',
#         type=str,
#         default=CONFIG
#     )

#     # Parse Args and config file
#     args = argsparser.parse_args()
#     config = ConfigParser()
#     try:
#         config.read(args.nagios_config)
#     except FileNotFoundError:
#         logging.warning(f'Unable to find file {args.nagios_config}, using \
# default config file.')
#         config.read(CONFIG)

#     # Set the nagios url based on args or config file
#     if args.nagiosurl is None:
#         nagiosurl = config.get('nagios', 'nagios')
#     else:
#         nagiosurl = args.nagiosurl

#     # Set api token based on args or config file
#     if args.token is None:
#         token = config.get('nagios', 'token')
#     else:
#         token = args.token

#     # Set the report date to yesterday
#     reportdate = datetime.today() - timedelta(days=1)
#     year = reportdate.year
#     month = reportdate.month
#     if month < 10:
#         month = f'0{month}'
#     day = reportdate.day
#     if day < 10:
#         day = f'0{day}'

#     # Determine the folder to retrieve reports from
#     path = f'{args.archivepath}/{year}/{month}/{day}/'

#     # Retrieve a list of all files in the directory
#     files = list_reports(path)
#     if len(files) < 1:
#         raise FileNotFoundError(f'No files for yesterday found in \
# {args.archivepath}, has dailyverification run?')

#     # Retrieve list of metrics from config file
#     metrics = (config.get('nagios', 'metrics')).split(',')
#     checkresults = nrdp.NagiosCheckResults()

#     # Loop through each report and append the results to the
#     # NagiosCheckResults object
#     for file in files:
#         checkresults += check_report_metrics(file, metrics)

#     # Submit the NagiosCheckResults object to Nagios's nrdp url
#     nrdp.submit(checkresults, nagiosurl, token, verify=False)


# # if __name__ == "__main__":
# #     main()
