from datetime import date
import subprocess
from stationverification import XML_CONVERTER
from obspy.io.xseed import Parser
import os
import requests


# ISPAQ
ispaqloc = "../../ISPAQ/ispaq/run_ispaq.py"
pfile = 'stationverification/data/eew_preferences.txt'
metrics = "eew_test"
pdfinterval = "aggregated"

# Station XML for QW
url = 'http://fdsn.seismo.nrcan.gc.ca/fdsnws/station/1/query?network=QW&level=response&nodata=404'  # noqa
request = requests.get(url, allow_redirects=True)
open('stationverification/data/QW.xml', 'wb').write(request.content)
station_url = "/nrn/home/NRN/haissa/workspace/station-validation-project/station-validation/stationverification/data/QW.xml"

# Apollo
station = "QW.QCC02.*.H??"
startdate = date(2022, 8, 1)
enddate = date(2022, 8, 2)
miniseedarchive = "/nrn/home/NRN/haissa/workspace/station-validation-project/station-validation/backupData/apolloLocation/archive/miniseed"

# Guralp
# station = "QW.BCC04.00.H??"
# startdate = date(2022, 9, 22)
# enddate = date(2022, 9, 23)
# miniseedarchive = "/nrn/home/NRN/haissa/workspace/station-validation-project/station-validation/backupData/guralp/archive/miniseed"


# Use IRIS's stationxml-seed-converter java porgram to convert stationxml
# to dataless seed, and then use the obspy parser object to convert to
# RESP file.
# tempfolder = tempfile.TemporaryDirectory(prefix='valdiation')

# Running with Station XML
subprocess.getoutput(
    f'java -jar {XML_CONVERTER} --input {station_url} --output \
        stationverification/data/stationXML.dataless')
pars = Parser("stationverification/data/stationXML.dataless")
if not os.path.isdir("stationverification/data/resp_files"):
    os.mkdir('stationverification/data/resp_files')
pars.write_resp(folder="stationverification/data/resp_files/", zipped=False)
resp_dir = "stationverification/data/resp_files/"

cmd = f'{ispaqloc} -M {metrics} \
    --starttime={startdate} --endtime={enddate} \
     -S {station} -P {pfile} \
        --pdf_interval {pdfinterval} \
        --station_url {station_url} \
        --dataselect_url {miniseedarchive}\
        --resp_dir {resp_dir}'

# Running with RESP file
# cmd = f'{ispaqloc} -M {metrics} \
#     --starttime={startdate} --endtime={enddate} \
#      -S {station} -P {pfile} \
#         --pdf_interval {pdfinterval} \
#         --dataselect_url {miniseedarchive}\
#         --resp_dir {resp_dir}'

proc = subprocess.Popen(
    cmd,
    shell=True
)
proc.wait()
