import subprocess
import os
import tempfile

from datetime import date
from obspy.io.xseed import Parser
from stationverification import XML_CONVERTER
from configparser import ConfigParser
from stationverification.utilities.prepare_ispaq import \
    InvalidConfigFile, prepare_ispaq_local


def handle_running_ispaq_command(
        ispaqloc: str,
        metrics: str,
        startdate: date,
        enddate: date,
        pfile: str,
        pdfinterval: str,
        miniseedarchive: str,
        network: str = None,
        station: str = None,
        location: str = None,
        station_url: str = None,
        stationconf: str = None):
    if stationconf is None:
        run_ispaq_command_with_stationXML(ispaqloc=ispaqloc,
                                          metrics=metrics,
                                          startdate=startdate,
                                          enddate=enddate,
                                          pfile=pfile,
                                          pdfinterval=pdfinterval,
                                          miniseedarchive=miniseedarchive,
                                          network=network,
                                          station=station,
                                          location=location,
                                          station_url=station_url)  # type: ignore # noqa
    else:
        run_ispaq_command_with_configfile(ispaqloc=ispaqloc,
                                          metrics=metrics,
                                          startdate=startdate,
                                          enddate=enddate,
                                          pfile=pfile,
                                          pdfinterval=pdfinterval,
                                          miniseedarchive=miniseedarchive,
                                          stationconf=stationconf)


def run_ispaq_command_with_stationXML(
        ispaqloc: str,
        metrics: str,
        startdate: date,
        enddate: date,
        pfile: str,
        pdfinterval: str,
        miniseedarchive: str,
        station_url: str,
        network: str = None,
        station: str = None,
        location: str = None,
        resp_dir: str = None):

    station_url_path = "stationverification/data/QW.xml"

    if location is None:
        snlc = f'{network}.{station}.*.H**'
    else:
        snlc = f'{network}.{station}.{location}.H**'
    subprocess.getoutput(f'java -jar {XML_CONVERTER} --input \
    {station_url_path} --output stationverification/data/stationXML.dataless')
    pars = Parser("stationverification/data/stationXML.dataless")
    if not os.path.isdir("stationverification/data/resp_files"):
        os.mkdir('stationverification/data/resp_files')
    pars.write_resp(
        folder="stationverification/data/resp_files/", zipped=False)

    resp_dir = "stationverification/data/resp_files/"

    cmd = f'{ispaqloc} -M {metrics} \
        --starttime={startdate} --endtime={enddate} \
        -S {snlc} -P {pfile} \
            --pdf_interval {pdfinterval} \
            --station_url {station_url_path} \
            --dataselect_url {miniseedarchive}\
            --resp_dir {resp_dir}'
    print("ISPAQ:", cmd)
    proc = subprocess.Popen(
        cmd,
        shell=True
    )
    proc.wait()


def run_ispaq_command_with_configfile(
        ispaqloc: str,
        metrics: str,
        startdate: date,
        enddate: date,
        pfile: str,
        pdfinterval: str,
        miniseedarchive: str,
        stationconf: str):

    stationconfiguration = ConfigParser()
    stationconfiguration.read(stationconf)
    if 'metadata' not in stationconfiguration.sections():
        raise InvalidConfigFile(
            f'No metadata section in {stationconf}')
    if 'station' not in stationconfiguration['metadata']:
        raise InvalidConfigFile(
            f'No station found in metadata section of {stationconf}')
    station = stationconfiguration.get('metadata', 'station')

    tempfolder = tempfile.TemporaryDirectory(prefix='valdiation')

    # Generate stationxml files and response files from the station config
    # file
    preffile = prepare_ispaq_local(
        stationconf=stationconfiguration,
        tempfolder=tempfolder.name,
        pfile=pfile,
        miniseed=miniseedarchive)

    cmd = f'{ispaqloc} -M {metrics} -S {station} --starttime={startdate} \
--endtime={enddate} -P {preffile} --pdf_interval {pdfinterval}'
    print("ISPAQ:", cmd)
    proc = subprocess.Popen(
        cmd,
        shell=True
    )
    proc.wait()
