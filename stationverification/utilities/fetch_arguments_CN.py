import argparse
from configparser import ConfigParser

from dateutil import parser as dateparser  # type: ignore

from stationverification.utilities import exceptions
from stationverification.config import get_default_parameters


class UserInput(dict):
    @property
    def station(self) -> bool:
        return self["station"]

    @property
    def network(self) -> str:
        return self["network"]

    @property
    def location(self) -> str:
        return self["location"]

    @property
    def startdate(self) -> list:
        return self["startdate"]

    @property
    def enddate(self) -> list:
        return self["enddate"]

    @property
    def ispaqloc(self) -> list:
        return self["ispaqloc"]

    @property
    def metrics(self) -> list:
        return self["metrics"]

    @property
    def pfile(self) -> list:
        return self["pfile"]

    @property
    def thresholds(self) -> list:
        return self["thresholds"]

    @property
    def latencyFiles(self) -> list:
        return self["latencyFiles"]

    @property
    def pdfinterval(self) -> list:
        return self["pdfinterval"]

    @property
    def station_url(self) -> list:
        return self["station_url"]

    @property
    def typeofinstrument(self) -> list:
        return self["typeofinstrument"]

    @property
    def miniseedarchive(self) -> list:
        return self["miniseedarchive"]

    @property
    def soharchive(self) -> list:
        return self["soharchive"]

    @property
    def outputdir(self) -> list:
        return self["outputdir"]

    @property
    def uploadresultstos3(self) -> list:
        return self["uploadresultstos3"]

    @property
    def bucketName(self) -> list:
        return self["bucketName"]

    @property
    def s3directory(self) -> list:
        return self["s3directory"]

    @property
    def stationconf(self) -> list:
        return self["stationconf"]


def fetch_arguments_CN() -> UserInput:
    # Create argparse object to handle user arguments
    argsparser = argparse.ArgumentParser()
    argsparser.add_argument(
        "-d",
        "--startdate",
        help="The first date of the verification period. Must be in YYYY-MM-DD \
format",
        type=str,
        required=True
    )
    argsparser.add_argument(
        "-e",
        "--enddate",
        help="The end of the verification period. Data will be tested for each \
day from the start date up to but not including the end date. Must be in \
YYYY-MM-DD format.",
        type=str,
        required=True
    )

    argsparser.add_argument(
        '-i',
        '--ispaqlocation',
        help='Specifies the path or alias for the ispaq cmdline tool. Default: \
ispaq',
        type=str,
    )

    argsparser.add_argument(
        '-L',
        '--location',
        help='The location code. I.e: 00',
        type=str,
    )
    argsparser.add_argument(
        '-m',
        '--miniseedarchive',
        help='The parent directory of the miniseed archive.',
        required=True
    )
    argsparser.add_argument(
        '-M',
        '--metrics',
        help='Select the group of metrics from the ispaq preference file to run with. \
Default: eew_test',
        type=str
    )
    argsparser.add_argument(
        '-N',
        '--network',
        help='The network code. I.e: QW',
        required=True,
        type=str,
    )
    argsparser.add_argument(
        '-o',
        '--outputdir',
        help='Output directory to store results in. If none is specified, the \
current directory is used.',
    )

    argsparser.add_argument(
        '-p',
        '--pdfinterval',
        help='time span for PDFs: daily and/or aggregated over the entire \
span',
        type=str
    )
    argsparser.add_argument(
        '-P',
        '--preference_file',
        help='The path to the preference file. Overrides the default ispaq\
 file.',
        type=str
    )

    argsparser.add_argument(
        '-S',
        '--station',
        help='The station code. I.e: QCC02',
        required=True,
        type=str,
    )
    argsparser.add_argument(
        '-t',
        '--thresholds',
        help='Overrides the default config file.',
        type=str
    )

    args = argsparser.parse_args()
    default_parameters = get_default_parameters()

    # Parameters required on every script call, with no default values
    station = args.station
    network = args.network
    startdate = (dateparser.parse(args.startdate, yearfirst=True)).date()
    enddate = (dateparser.parse(args.enddate, yearfirst=True)).date()

    # Config files
    pfile = args.preference_file if args.preference_file is not None\
        else default_parameters.PREFERENCE_FILE
    thresholds = ConfigParser()
    if args.thresholds is not None:
        thresholds.read(args.thresholds)
    else:
        thresholds.read(default_parameters.THRESHOLDS)

    # Directories, with default paths
    ispaqloc = args.ispaqlocation if args.ispaqlocation is not None\
        else default_parameters.ISPAQ_LOCATION

    miniseedarchive = args.miniseedarchive

    outputdir = args.outputdir if args.outputdir is not None\
        else default_parameters.OUTPUT_DIRECTORY

    # Optional parameters, with default value
    metrics = args.metrics if args.metrics is not None\
        else default_parameters.METRICS
    pdfinterval = args.pdfinterval if args.pdfinterval is not None\
        else default_parameters.PDF_INTERVAL

    # Optional parameters, with no default value
    location = args.location

    if startdate > enddate:
        raise exceptions.TimeSeriesError('Enddate must be after startdate.')
    elif startdate == enddate:
        raise exceptions.TimeSeriesError('Enddate is not inclusive. To test for one day, set \
the enddate to the day after the startdate')

    return UserInput(station=station,
                     network=network,
                     location=location,
                     startdate=startdate,
                     enddate=enddate,
                     ispaqloc=ispaqloc,
                     metrics=metrics,
                     pfile=pfile,
                     thresholds=thresholds,
                     pdfinterval=pdfinterval,
                     miniseedarchive=miniseedarchive,
                     outputdir=outputdir)
