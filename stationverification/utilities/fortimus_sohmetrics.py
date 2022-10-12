import logging
import subprocess
import re
import numpy as np
from configparser import ConfigParser
from datetime import date, timedelta
from typing import Any, List
from . import sohmetrics
from stationverification.utilities import exceptions
from stationverification.utilities.plot_clock_offset import plot_clock_offset
from stationverification.utilities.plot_DAC_voltage import plot_DAC_voltage


class FortmisMetricResults(dict):
    @property
    def result(self) -> bool:
        return self["result"]

    @property
    def details(self) -> str:
        return self["details"]


def get_fortimus_soh_files(
        network: str,
        station: str,
        startdate: date,
        enddate: date,
        soh_directory: str,
        location: Any = None) -> List[str]:
    '''
    Retrieves a list of the daily fortimus SOH files

    Parameters
    ----------
    network: str
        Network Code
    station: str
        Station Code
    startdate: date
        The first day to search for files for
    enddate: date
        The end date for the search, non-inclusive
    soh_directory: str
        The directory where the soh archive should be found

    Returns
    -------
    list
        List of files found for the specified station during the specified time
        period
    '''
    files: List[str] = []
    iterdate = startdate
    if location is None:
        snlc = f'{network}.{station}.*.SOH'
    else:
        snlc = f'{network}.{station}.{location}.SOH'
    # Loop through all the dates
    while iterdate < enddate:
        # Get the julian day and convert it to a 3 digit string
        jday = "%03d" % iterdate.timetuple().tm_yday
        # Search for the file for the specific day
        command = f'ls {soh_directory}/{iterdate.strftime("%Y/%m/%d")}/{snlc}\
.{iterdate.year}.{jday} 2>/dev/null'
        logging.debug(command)
        output = subprocess.getoutput(command)
        if len(output) > 0:
            # Add the file to a list
            files = files + output.split('\n')

        iterdate = iterdate + timedelta(days=+1)
    # Raise an error if no files were collected
    if len(files) < 1:
        logging.warning(f'No SOH files found for {iterdate}')
    logging.debug(
        f'{len(files)} files found for {network}.{station} \
between {startdate} and {enddate}')
    return files


def handle_fortimus_soh_miniseed_metrics(
        network: str,
        station: str,
        startdate: date,
        enddate: date,
        miniseed_directory: str,
        json_dict: dict,
        timingSource: str,
        location: Any = None) -> dict:
    '''
    Retrieves a list of the daily SOH channel files for the specified SOH
    channel

    Parameters
    ----------
    network: str
        Network Code
    station: str
        Station Code
    startdate: date
        The first day to search for files for
    enddate: date
        The end date for the search, non-inclusive
    soh_directory: str
        The directory where the soh archive should be found

    Returns
    -------
    Tuple
        Results from each miniseed files used for SOH metrics
    '''
    try:
        clock_offset_sohfiles = \
            sohmetrics.getsohfiles(network=network,
                                   station=station,
                                   location=location,
                                   startdate=startdate,
                                   enddate=enddate,
                                   channel="LEO" if timingSource.lower() == "gnss" else "LEP",  # noqa
                                   soh_directory=miniseed_directory)
        clock_offset_merged_streams =\
            sohmetrics.get_list_of_streams_from_list_of_files(
                clock_offset_sohfiles)
        clock_offset_metric_result = \
            validate_clock_offset_metric(
                clock_offset_merged_streams=clock_offset_merged_streams,
                clock_offset_threshold_in_microseconds=100.0)
        json_dict = \
            add_fortimus_soh_miniseed_metric_results_to_report(
                clock_offset_metric_result=clock_offset_metric_result,
                current_json_report=json_dict)

        plot_clock_offset(
            list_of_streams=clock_offset_merged_streams,
            clock_offset_threshold_in_microseconds=100.0,
            network=network,
            station=station,
            startdate=startdate,
            enddate=enddate,
            location=location
        )
    except exceptions.StreamError as e:
        logging.error(e)
        logging.warning(
            'LEO data does not exist. Skipping clock offset metric.')
    try:
        DAC_voltage_sohfiles = \
            sohmetrics.getsohfiles(network=network,
                                   station=station,
                                   location=location,
                                   startdate=startdate,
                                   enddate=enddate,
                                   channel="LED",
                                   soh_directory=miniseed_directory)
        DAC_voltage_merged_streams =\
            sohmetrics.get_list_of_streams_from_list_of_files(
                DAC_voltage_sohfiles)
        plot_DAC_voltage(list_of_streams=DAC_voltage_merged_streams)
    except exceptions.StreamError as e:
        logging.error(e)
        logging.warning(
            'LED data does not exist. Skipping DAC Voltage Plot.')
    return json_dict


def validate_clock_offset_metric(
        clock_offset_merged_streams: List,
        clock_offset_threshold_in_microseconds: float) -> FortmisMetricResults:
    '''
    The raw channel values are in counts and should be multiplied
    by the calibration value of 24.112654 to get a number of
    nanoseconds of offset. The timing quality will remain
    'fine locked' as long as the time offset from the time source
    is within half of a sample period. The system is operating in
    5000 samples per second so as long as the time difference
    is kept within 100000ns (1s / 5000sps / 2) there is no threat
    to the sample timing precision.

    We will automatically fail the validation if one entry is
    above the threshold
    '''

    final_metric_result = FortmisMetricResults(
        result=True, details="")
    for data in clock_offset_merged_streams:
        trace = data[0]
        offsets = (abs((trace.data * 24.112654) / 1000))
        maximum_offset = np.amax(offsets)
        date_of_offset = re.findall(
            "([^T]*)", f'{trace.stats.starttime}')[0]
        if maximum_offset >= clock_offset_threshold_in_microseconds:
            final_metric_result = FortmisMetricResults(
                result=False,
                details=f"The clock offset was above the threshold of \
{clock_offset_threshold_in_microseconds} microseconds on {date_of_offset}")
    return final_metric_result


def get_fine_locked_percentage(data: List) -> float:
    length_of_data = len(data)
    number_of_times_clock_is_fine_locked = np.count_nonzero(data == 0)
    percentage_data_is_fined_locked = \
        round(number_of_times_clock_is_fine_locked /
              length_of_data * 100, 2)
    return percentage_data_is_fined_locked


def add_fortimus_soh_metric_results_to_json(soh_data: List[Any],
                                            json_dict: dict,
                                            thresholds: ConfigParser) -> dict:
    number_of_satellites_metric_result,\
        clock_quality_metric_result,\
        clock_locked_metric_result\
        = validate_fortimus_soh_metrics(
            soh_data=soh_data,
            thresholds=thresholds)

    # Add the results to the JSON
    json_dict =\
        add_fortimus_soh_metric_results_to_report(
            number_of_satellites_metric_result=number_of_satellites_metric_result,  # noqa
            current_json_report=json_dict,
            clock_quality_metric_result=clock_quality_metric_result,
            clock_locked_metric_result=clock_locked_metric_result
        )
    return json_dict


def validate_fortimus_soh_metrics(soh_data: List[Any],
                                  thresholds: ConfigParser):
    number_of_satellites_threshold = thresholds.getfloat(
        'thresholds', 'satellites_locked', fallback=6)
    number_of_satellites_used_metric_result = FortmisMetricResults(
        result=True,
        details=f"Number of satellites used was always above the \
threshold of {number_of_satellites_threshold}")
    clock_quality_metric_result = FortmisMetricResults(
        result=True, details="Clock was always Fine locked")
    clock_locked_metric_result = FortmisMetricResults(
        result=True, details="Clock was always locked")
    for data in soh_data:
        number_of_satellites_used_metric_result \
            = validate_number_of_satellites_metric(
                data=data["number_of_satellites_used"],
                number_of_satellites_threshold=number_of_satellites_threshold,
                current_metric_results=number_of_satellites_used_metric_result,
                current_file=data["file"])
        clock_quality_metric_result \
            = validate_clock_quality_metric(
                data=data["timing_quality"],
                current_metric_results=clock_quality_metric_result,
                current_file=data["file"])
        clock_locked_metric_result \
            = validate_clock_locked_metric(
                data=data["clock_locked_status"],
                current_metric_results=clock_locked_metric_result,
                current_file=data["file"])
    return number_of_satellites_used_metric_result,\
        clock_quality_metric_result,\
        clock_locked_metric_result


def validate_number_of_satellites_metric(
        data: List[int],
        number_of_satellites_threshold: float,
        current_metric_results: FortmisMetricResults,
        current_file: str) -> FortmisMetricResults:
    final_metric_result = current_metric_results
    for d in data:
        if d < number_of_satellites_threshold:
            final_metric_result = FortmisMetricResults(
                result=False,
                details=f'Number of satellites was below the threshold of\
 {number_of_satellites_threshold}. Check file {current_file}')
    return final_metric_result


def validate_clock_quality_metric(
        data: List[int],
        current_metric_results: FortmisMetricResults,
        current_file: str) -> FortmisMetricResults:
    final_metric_result = current_metric_results
    for d in data:
        if d != "Fine locked":
            final_metric_result = FortmisMetricResults(
                result=False,
                details=f'Clock is not Fine Locked. Check file {current_file}')
    return final_metric_result


def validate_clock_locked_metric(
        data: List[int],
        current_metric_results: FortmisMetricResults,
        current_file: str) -> FortmisMetricResults:
    final_metric_result = current_metric_results
    for d in data:
        if d != "Locked":
            final_metric_result = FortmisMetricResults(
                result=False,
                details=f'Clock is not Locked. Check file {current_file}')
    return final_metric_result


def add_fortimus_soh_metric_results_to_report(
        number_of_satellites_metric_result: FortmisMetricResults,
        current_json_report: dict,
        clock_quality_metric_result: FortmisMetricResults,
        clock_locked_metric_result: FortmisMetricResults
):
    json_report_with_soh_data = current_json_report
    json_report_with_soh_data['satellites_locked'] = {}
    json_report_with_soh_data['satellites_locked']['passed'] = \
        number_of_satellites_metric_result.result
    json_report_with_soh_data['satellites_locked']['details'] = \
        number_of_satellites_metric_result.details

    json_report_with_soh_data['timing_quality'] = {}
    json_report_with_soh_data['timing_quality']['passed'] = \
        clock_quality_metric_result.result
    json_report_with_soh_data['timing_quality']['details'] = \
        clock_quality_metric_result.details

    json_report_with_soh_data['clock_locked'] = {}
    json_report_with_soh_data['clock_locked']['passed'] = \
        clock_locked_metric_result.result
    json_report_with_soh_data['clock_locked']['details'] = \
        clock_locked_metric_result.details

    return json_report_with_soh_data


def add_fortimus_soh_miniseed_metric_results_to_report(
        current_json_report: dict,
        clock_offset_metric_result: FortmisMetricResults
):
    json_report_with_soh_miniseed_data = current_json_report

    json_report_with_soh_miniseed_data['clock_offset'] = {}
    json_report_with_soh_miniseed_data['clock_offset']['passed'] = \
        clock_offset_metric_result.result
    json_report_with_soh_miniseed_data['clock_offset']['details'] = \
        clock_offset_metric_result.details

    return json_report_with_soh_miniseed_data
