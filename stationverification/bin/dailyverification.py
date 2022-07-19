# '''
# This module is designed to do a daily, one-day Ispaq check on every station in
# the verification facility so that the results can be injected into Ispaq
# '''
# import argparse
# from stationverification import ISPAQ_PREF
# from stationverification import CONFIG
# from stationverification import STATION_XML
# from stationverification.utilities.generate_report import gather_stats
# # from stationverification.utilities.generate_report import bulk_report
# import logging
# import os
# import subprocess
# from datetime import date, timedelta
# import tempfile

# flake8: noqa

# def main():
#     argsparser = argparse.ArgumentParser()
#     argsparser.add_argument(
#         '-i',
#         '--ispaqlocation',
#         default='ispaq',
#         help='If ispaq is not installed as a package, specify the location of \
# run_ispaq.py Default: ispaq',
#         type=str
#     )
#     argsparser.add_argument(
#         '-P',
#         '--preference_file',
#         default=ISPAQ_PREF,
#         help=f'Declare what ISPAQ preference file to use when running ISPAQ. \
# Default is eew_preferences.txt. Default: {ISPAQ_PREF}',
#         type=str
#     )
#     argsparser.add_argument(
#         '-L',
#         '--logfile',
#         default=None,
#         help='To log to a file instead of stdout, specify the filename.',
#         type=str
#     )
#     argsparser.add_argument(
#         '-v',
#         '--verbose',
#         action='store_true',
#         help='Sets logging level to DEBUG'
#     )
#     argsparser.add_argument(
#         '-t',
#         '--thresholds',
#         default=CONFIG,
#         help=f'The path to the preference file containing the thresholds to \
# test the metrics against. Default: {CONFIG}',
#         type=str
#     )
#     argsparser.add_argument(
#         '-l',
#         '--HDF5',
#         help='The directory containing HDF5 sniffwave files. Default: \
# /data/sniffwave',
#         type=str,
#         default='/data/sniffwave'
#     )
#     argsparser.add_argument(
#         '-a',
#         '--archive',
#         type=str,
#         help='The path to the miniseed archive. Default: /data/miniseed',
#         default='/data/miniseed'
#     )
#     argsparser.add_argument(
#         '-f',
#         '--fdsnws',
#         help='Specity a FDSNWS to use for waveform data instead of a miniseed \
# archive.',
#         type=str,
#         default=None
#     )
#     argsparser.add_argument(
#         '-o',
#         '--outputdirectory',
#         type=str,
#         default='./dailyverification',
#         help='The directory to archive daily verification reports. Default: \
# ./dailyverification'
#     )
#     args = argsparser.parse_args()

#     # If a logfile is specified, set up logging to use it
#     if args.logfile is not None:
#         logging.basicConfig(
#             format='%(asctime)s:%(levelname)s:%(message)s',
#             datefmt="%Y-%m-%d %H:%M:%S",
#             level=logging.DEBUG if args.verbose else logging.INFO,
#             filename=args.logfile, filemode='w')
#     else:
#         logging.basicConfig(
#             format='%(asctime)s:%(levelname)s:%(message)s',
#             datefmt="%Y-%m-%d %H:%M:%S",
#             level=logging.DEBUG if args.verbose else logging.INFO)

#     startdate = date.today() + timedelta(days=-1)
#     enddate = date.today()

#     ispaqloc = args.ispaqlocation

#     metrics = 'eew_no_psd'

#     pfile = args.preference_file
#     # fdsnws = args.fdsnws

#     temppref = tempfile.NamedTemporaryFile('w+b')
#     with open(pfile, "r") as preffile:
#         contents = preffile.readlines()
#     linenum = contents.index('Data_Access:\n') + 2
#     contents[linenum] = f'  dataselect_url:  {args.archive}/\n'
#     contents[linenum+1] = f'  station_url:  {STATION_XML}\n'
#     contents[linenum+2] = '  event_url:  IRIS\n'
#     contents[linenum+3] = '  resp_dir:  \n'
#     contents = "".join(contents)
#     temppref.write(contents.encode())
#     temppref.seek(0, os.SEEK_CUR)

#     cmd = f'{ispaqloc} -M {metrics} -S all --starttime={startdate} \
# --endtime={enddate} -P {temppref.name}'

#     proc = subprocess.Popen(
#         cmd,
#         shell=True,
#         # stdout=subprocess.PIPE,
#         # stderr=subprocess.PIPE
#     )
#     proc.wait()

#     stationmetricdata = gather_stats(
#         start=startdate,
#         stop=enddate,
#         metrics=metrics
#     )

#     bulk_report(
#         stationmetricdata,
#         args.HDF5,
#         args.outputdirectory,
#         startdate
#     )


# # if __name__ == "__main__":
# #     main()
