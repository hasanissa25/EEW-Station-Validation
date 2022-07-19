from datetime import date

from stationverification.utilities import sohmetrics
from configparser import ConfigParser

network = "QW"
station = "QCC02"
startdate = date(2022, 3, 28)
enddate = date(2022, 4, 5)
directory = 'tests/data/apollo/archive/soh'
thresholds = ConfigParser()
thresholds.read('tests/data/config.ini')
timing_quality_sohfiles = sohmetrics.getsohfiles(network=network,
                                                 station=station,
                                                 startdate=startdate,
                                                 enddate=enddate,
                                                 channel="LCQ",
                                                 directory=directory)
timing_quality_merged_streams =\
    sohmetrics.get_list_of_streams_from_list_of_files(
        timing_quality_sohfiles)


results = sohmetrics.check_timing_quality(
    list_of_streams=timing_quality_merged_streams,
    threshold=thresholds.getfloat(
        'thresholds', 'timing_quality', fallback=70.0),
    startdate=startdate, enddate=enddate, network=network,
    station=station,
)

clock_offset_sohfiles = sohmetrics.getsohfiles(network=network,
                                               station=station,
                                               startdate=startdate,
                                               enddate=enddate,
                                               channel="LCE",
                                               directory=directory)
clock_offset_merged_streams =\
    sohmetrics.get_list_of_streams_from_list_of_files(
        clock_offset_sohfiles)
results = sohmetrics.check_clock_offset(
    list_of_streams=clock_offset_merged_streams,
    threshold=thresholds.getfloat(
        'thresholds', 'clock_offset', fallback=0.100),
    startdate=startdate,
    enddate=enddate,
    network=network,
    station=station
)
