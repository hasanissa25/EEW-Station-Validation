from stationverification.utilities import exceptions
from datetime import date
from stationverification.utilities.plot_clock_offset import plot_clock_offset
import logging
from . import sohmetrics
from configparser import ConfigParser
from typing import Any


def add_soh_results_to_report(network: str,
                              station: str,
                              location: Any,
                              startdate: date,
                              enddate: date,
                              directory: str,
                              typeofinstrument: str,
                              json_dict: dict,
                              thresholds: ConfigParser):
    clock_locked_data = None
    clock_offset_data = None
    try:
        clock_offset_sohfiles = sohmetrics.getsohfiles(network=network,
                                                       station=station,
                                                       location=location,
                                                       startdate=startdate,
                                                       enddate=enddate,
                                                       channel="LCE",
                                                       directory=directory)
        clock_offset_merged_streams =\
            sohmetrics.get_list_of_streams_from_list_of_files(
                clock_offset_sohfiles)
        clock_offset_data = sohmetrics.get_list_of_data_from_list_of_streams(
            clock_offset_merged_streams)
        clock_offset_results = sohmetrics.check_clock_offset(
            list_of_streams=clock_offset_merged_streams,
            threshold=thresholds.getfloat(
                'thresholds', 'clock_offset', fallback=1),
            startdate=startdate)

        if clock_offset_results is not None:
            json_dict['clock_offset'] = {}
            json_dict['clock_offset']['passed'] = clock_offset_results.passed
            json_dict['clock_offset']['values'] = clock_offset_results.results
            if clock_offset_results.passed is False:
                json_dict['clock_offset']['details'] = \
                    clock_offset_results.details
    except exceptions.StreamError as e:
        logging.error(e)
        logging.warning(
            'LCE data does not exist. Skipping clock offset metric.')

    try:
        check_clock_locked_sohfiles = \
            sohmetrics.getsohfiles(network=network,
                                   station=station,
                                   location=location,
                                   startdate=startdate,
                                   enddate=enddate,
                                   channel="GST",
                                   directory=directory)
        check_clock_locked_merged_streams =\
            sohmetrics.get_list_of_streams_from_list_of_files(
                check_clock_locked_sohfiles)
        clock_locked_data = sohmetrics.get_list_of_data_from_list_of_streams(
            check_clock_locked_merged_streams)
        clock_locked_results = sohmetrics.check_clock_locked(
            list_of_streams=check_clock_locked_merged_streams,
            threshold=thresholds.getfloat(
                'thresholds', 'clock_locked', fallback=6),
            startdate=startdate
        )

        if clock_locked_results is not None:
            json_dict['clock_locked'] = {}
            json_dict['clock_locked']['passed'] = clock_locked_results.passed
            json_dict['clock_locked']['values'] = clock_locked_results.results
            if clock_locked_results.passed is False:
                json_dict['clock_locked']['details'] = \
                    clock_locked_results.details
    except exceptions.StreamError as e:
        logging.error(e)
        logging.warning(
            'GST data does not exist. Skipping clock locked metric.')
    if clock_locked_data is not None and clock_offset_data is not None:
        plot_clock_offset(network=network,
                          station=station,
                          startdate=startdate,
                          enddate=enddate,
                          results=(clock_locked_data, clock_offset_data),
                          threshold=thresholds.getfloat(
                              'thresholds', 'clock_offset', fallback=1),
                          location=location
                          )

    try:
        timing_quality_sohfiles = sohmetrics.getsohfiles(network=network,
                                                         station=station,
                                                         location=location,
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
            location=location

        )

        if results is not None:
            json_dict['timing_quality'] = {}
            json_dict['timing_quality']['passed'] = results.passed
            json_dict['timing_quality']['values'] = results.results
            if results.passed is False:
                json_dict['timing_quality']['details'] = results.details
            # plot the timing quality results

    except exceptions.StreamError as e:
        logging.error(e)
        logging.warning(
            'LCQ data does not exist. Skipping timing quality metric.')

    try:
        check_number_of_satellites_sohfiles = \
            sohmetrics.getsohfiles(network=network,
                                   station=station,
                                   location=location,
                                   startdate=startdate,
                                   enddate=enddate,
                                   channel="GNS",
                                   directory=directory)
        check_number_of_satellites_merged_streams =\
            sohmetrics.get_list_of_streams_from_list_of_files(
                check_number_of_satellites_sohfiles)
        results = sohmetrics.check_number_of_satellites(
            list_of_streams=check_number_of_satellites_merged_streams,
            threshold=thresholds.getfloat(
                'thresholds', 'satellites_locked', fallback=6),
            startdate=startdate
        )

        if results is not None:
            json_dict['satellites_locked'] = {}
            json_dict['satellites_locked']['passed'] = results.passed
            # Since were getting the average of a list of size 1, \
            # were only returning the first element of the list
            json_dict['satellites_locked']['values'] = results.results
            if results.passed is False:
                json_dict['satellites_locked']['details'] = results.details
    except exceptions.StreamError as e:
        logging.error(e)
        logging.warning(
            'GNS data does not exist. Skipping number of satellites metric.')
    return json_dict
