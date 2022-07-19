import subprocess
import os

from datetime import date
from obspy.io.xseed import Parser
from stationverification import XML_CONVERTER


def handle_running_ispaq_command_CN(
        ispaqloc: str,
        metrics: str,
        startdate: date,
        enddate: date,
        pfile: str,
        pdfinterval: str,
        miniseedarchive: str,
        network: str = None,
        station: str = None):
    run_ispaq_command_with_stationXML(ispaqloc=ispaqloc,
                                      metrics=metrics,
                                      startdate=startdate,
                                      enddate=enddate,
                                      pfile=pfile,
                                      pdfinterval=pdfinterval,
                                      miniseedarchive=miniseedarchive,
                                      network=network,
                                      station=station)


def run_ispaq_command_with_stationXML(
        ispaqloc: str,
        metrics: str,
        startdate: date,
        enddate: date,
        pfile: str,
        pdfinterval: str,
        miniseedarchive: str,
        network: str = None,
        station: str = None):

    station_url_path = "stationverification/data/CN.xml"

    snlc = f'{network}.{station}.*.***'

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
