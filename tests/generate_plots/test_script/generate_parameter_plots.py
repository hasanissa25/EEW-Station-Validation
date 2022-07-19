from stationverification.utilities.generate_report import gather_stats
from datetime import date
from stationverification.utilities.generate_plots import plot_metrics,\
    PlotParameters
import subprocess
from stationverification import XML_CONVERTER
import os
from obspy.io.xseed import Parser

network = "QW"
station = "QCC02"
startdate = date(2022, 4, 1)
enddate = date(2022, 4, 6)
metrics = "eew_test"
pfile = 'stationverification/data/eew_preferences.txt'
miniseedarchive = "tests/data/apollo/archive/miniseed"
ispaqloc = "../ISPAQ/ispaq/run_ispaq.py"
pdfinterval = "aggregated"
station_url = "stationverification/data/QW.xml"

subprocess.getoutput(f'java -jar {XML_CONVERTER} --input \
{station_url} --output stationverification/data/stationXML.dataless')
pars = Parser("stationverification/data/stationXML.dataless")
if not os.path.isdir("stationverification/data/resp_files"):
    os.mkdir('stationverification/data/resp_files')
pars.write_resp(
    folder="stationverification/data/resp_files/", zipped=False)

resp_dir = "stationverification/data/resp_files/"
# Run the ispaq command to gather basic stats
# Add '--sds_files' for earthworm files
cmd = f'{ispaqloc} -M {metrics} \
    --starttime={startdate} --endtime={enddate} \
    -S {network}.{station}.*.H** -P {pfile} \
        --pdf_interval {pdfinterval} \
        --station_url {station_url} \
        --dataselect_url {miniseedarchive}\
        --resp_dir {resp_dir}'
proc = subprocess.Popen(
    cmd,
    shell=True
)
proc.wait()


stationMetricData = gather_stats(
    snlc=f'{network}.{station}.x.Hxx',
    start=startdate,
    stop=enddate,
    metrics=metrics)
for channel in stationMetricData.get_channels(
    network=network,
    station=station
):
    plot_metrics(
        PlotParameters(network=network,
                       station=station,
                       channel=channel,
                       stationMetricData=stationMetricData,
                       start=startdate,
                       stop=enddate)

    )
