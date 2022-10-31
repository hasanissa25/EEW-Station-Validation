import argparse
from configparser import ConfigParser

from dateutil import parser as dateparser  # type: ignore

from stationverification.utilities import exceptions

from stationverification.config import get_default_parameters

from stationverification.utilities.fetch_type_of_instrument_from_stationxml \
    import fetch_type_of_instrument_from_stationxml


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
    def startdate(self) -> str:
        return self["startdate"]

    @property
    def enddate(self) -> str:
        return self["enddate"]

    @property
    def ispaqloc(self) -> str:
        return self["ispaqloc"]

    @property
    def metrics(self) -> str:
        return self["metrics"]

    @property
    def pfile(self) -> str:
        return self["pfile"]

    @property
    def thresholds(self) -> str:
        return self["thresholds"]

    @property
    def latencyFiles(self) -> str:
        return self["latencyFiles"]

    @property
    def pdfinterval(self) -> str:
        return self["pdfinterval"]

    @property
    def station_url(self) -> str:
        return self["station_url"]

    @property
    def typeofinstrument(self) -> str:
        return self["typeofinstrument"]

    @property
    def miniseedarchive(self) -> str:
        return self["miniseedarchive"]

    @property
    def soharchive(self) -> str:
        return self["soharchive"]

    @property
    def outputdir(self) -> str:
        return self["outputdir"]

    @property
    def uploadresultstos3(self) -> str:
        return self["uploadresultstos3"]

    @property
    def bucketName(self) -> str:
        return self["bucketName"]

    @property
    def s3directory(self) -> str:
        return self["s3directory"]

    # @property
    # def stationconf(self) -> list:
    #     return self["stationconf"]

    @property
    def timingSource(self) -> str:
        return self["timingSource"]

    @property
    def updateStationXml(self) -> bool:
        return self["updateStationXml"]

    @property
    def instrument_gain(self) -> str:
        return self["instrument_gain"]


def fetch_arguments() -> UserInput:
    # Create argparse object to handle user arguments
    argsparser = argparse.ArgumentParser()
    argsparser.add_argument(
        "-b",
        "--s3bucketname",
        help="To which bucket to upload in S3",
        type=str,

    )
    argsparser.add_argument(
        "-B",
        "--s3bucketpathtosaveto",
        help="Which 'directory' in S3 to save to",
        type=str,
    )
    # argsparser.add_argument(
    #     '-c',
    #     '--stationconfig',
    #     help='Path to the file that contains station information.',
    #     type=str,
    # )
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
#     argsparser.add_argument(
#         '-f',
#         '--fdsnws',
#         help='FDSN webservice URL to use. If not specified, then \
# --stationconfig must be specified to generate station metadata for Ispaq',
#         type=str,
#         default=None
#     )
    argsparser.add_argument(
        '-H',
        '--soh_archive',
        help='Path to the state of health files',
        type=str,
    )
    argsparser.add_argument(
        '-i',
        '--ispaqlocation',
        help='Specifies the path or alias for the ispaq cmdline tool. Default: \
ispaq',
        type=str,
    )
    argsparser.add_argument(
        '-l',
        '--latency',
        help='The directory containing the latency data.',
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
        '-s',
        '--station_url',
        help='FDSN webservice or path to stationXML file',
        type=str,
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
    argsparser.add_argument(
        '-T',
        '--timingSource',
        help='Timing source for Fortimus instruments. Either GNSS or PTP.\
Defaults to GNSS',
        type=str
    )
    # argsparser.add_argument(
    #     '-T',
    #     '--typeofinstrument',
    #     help='type of instrument used, APOLLO or GURALP',
    #     required=True,
    #     type=str
    # )
    argsparser.add_argument(
        '-U',
        '--uploadresultstos3',
        help='True, or False. If set to True, the results will be \
        automatically uploaded to s3 bucket',
        type=bool
    )
    argsparser.add_argument(
        '-u',
        '--updateStationXml',
        help='True, or False. If set to True, an updated station xml will be \
fetched from the FDSN. Defaults to False',
        type=bool,
        default=False
    )

    argsparser.add_argument(
        '-g',
        '--gain',
        help='Instrument gain',
        type=str,
    )

    args = argsparser.parse_args()
    default_parameters = get_default_parameters()

    # Parameters required on every script call, with no default values
    station = args.station
    network = args.network
    startdate = (dateparser.parse(args.startdate, yearfirst=True)).date()
    enddate = (dateparser.parse(args.enddate, yearfirst=True)).date()

    # Only one of them is required, either station_url or stationconf
    station_url = args.station_url if args.station_url is not None\
        else default_parameters.STATION_URL
    # stationconf = args.stationconfig if args.stationconfig is not None\
    #     else default_parameters.STATION_CONFIG
    typeofinstrument = fetch_type_of_instrument_from_stationxml(
        network=network,
        station=station,
        station_xml=station_url)

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

    latencyFiles = args.latency if args.latency is not None\
        else default_parameters.APOLLO_LATENCY_ARCHIVE \
        if typeofinstrument.lower() == "titansma" \
        else default_parameters.GURALP_LATENCY_ARCHIVE
    miniseedarchive = args.miniseedarchive if args.miniseedarchive is not None\
        else default_parameters.APOLLO_MINISEED_ARCHIVE \
        if typeofinstrument.lower() == "titansma" \
        else default_parameters.GURALP_MINISEED_ARCHIVE
    soharchive = args.soh_archive if args.soh_archive is not None\
        else default_parameters.APOLLO_SOH_ARCHIVE \
        if typeofinstrument.lower() == "titansma" \
        else default_parameters.GURALP_SOH_ARCHIVE
    outputdir = args.outputdir if args.outputdir is not None\
        else default_parameters.OUTPUT_DIRECTORY
    s3directory = args.s3bucketpathtosaveto \
        if args.s3bucketpathtosaveto is not None\
        else default_parameters.S3_DIRECTORY

    # Optional parameters, with default value
    metrics = args.metrics if args.metrics is not None\
        else default_parameters.METRICS
    pdfinterval = args.pdfinterval if args.pdfinterval is not None\
        else default_parameters.PDF_INTERVAL
    bucketName = args.s3bucketname if args.s3bucketname is not None\
        else default_parameters.S3_BUCKET_NAME
    timingSource = args.timingSource if args.timingSource is not None\
        else default_parameters.TIMING_SOURCE
    updateStationXml = args.updateStationXml

    # Optional parameters, with no default value
    uploadresultstos3 = args.uploadresultstos3
    location = args.location
    # fdsnws = args.fdsnws
    instrument_gain = args.gain

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
                     latencyFiles=latencyFiles,
                     pdfinterval=pdfinterval,
                     station_url=station_url,
                     typeofinstrument=typeofinstrument,
                     miniseedarchive=miniseedarchive,
                     soharchive=soharchive,
                     outputdir=outputdir,
                     uploadresultstos3=uploadresultstos3,
                     bucketName=bucketName,
                     s3directory=s3directory,
                     timingSource=timingSource,
                     updateStationXml=updateStationXml,
                     #  stationconf=stationconf
                     instrument_gain=instrument_gain
                     )
