# flake8: noqa
import obspy
import pytest
import subprocess

import numpy as np
import numpy.ma as ma

from typing import List
from datetime import date

from stationverification.utilities import exceptions, sohmetrics


def test_getsohfiles(sohcriteria: dict):
    testresults_files_found = sohmetrics.getsohfiles(
        network=sohcriteria["network"],
        station=sohcriteria["station"],
        channel=sohcriteria["channel"],
        startdate=sohcriteria["startdate"],
        enddate=sohcriteria["enddate"],
        directory=sohcriteria["directory"])
    assert testresults_files_found == [
        'tests/data/apollo/archive/soh/2022/04/01/QW.QCC02..LCQ.2022.091']

    testresults_files_not_found = sohmetrics.getsohfiles(
        network=sohcriteria["network"],
        station="non_existent",
        channel=sohcriteria["channel"],
        startdate=sohcriteria["startdate"],
        enddate=sohcriteria["enddate"],
        directory=sohcriteria["directory"])
    assert testresults_files_not_found == []


def test_get_list_of_streams_from_list_of_files(example_files: List[str]):
    list_of_streams = sohmetrics.get_list_of_streams_from_list_of_files(
        example_files)
    assert (list_of_streams[0][0].data == [1, 2, 3]).all()
    assert (list_of_streams[1][0].data == [5, 6, 7]).all()
    assert (list_of_streams[2][0].data == [1, 2, 3, 5, 6, 7]).all()

    with pytest.raises(exceptions.StreamError):
        sohmetrics.get_list_of_streams_from_list_of_files(
            [])


def test_getstats(stream_with_gaps: obspy.Stream):
    '''
    Gathers statistics from a SOH miniseed file

    Returns:
        tuple:
            Average, Minimum, and Maximum values for the SOH file
    '''

    stats = sohmetrics.getstats(
        stream=stream_with_gaps)

    assert stats.average == 4
    assert stats.minimum == 1
    assert stats.maximum == 7


def test_get_merged_stream(stream_with_gaps: obspy.Stream,
                           stream_without_gaps: obspy.Stream,
                           empty_stream: obspy.Stream):
    # Stream with gaps
    mergedstream = sohmetrics.get_merged_stream(stream_with_gaps)
    merged_stream_data = sohmetrics.get_stream_data_of_merged_streams(
        mergedstream)
    expected_masked_trace = ma.array(
        [1, 2, 3, 4, 5, 6, 7], mask=[0, 0, 0, 1, 0, 0, 0])
    assert (merged_stream_data == expected_masked_trace).all()

    # Stream without gaps
    mergedstream = sohmetrics.get_merged_stream(
        stream_without_gaps)
    merged_stream_data = sohmetrics.get_stream_data_of_merged_streams(
        mergedstream)

    expected_trace = np.array([1, 2, 3])

    assert (merged_stream_data == expected_trace).all()

    # Empty stream
    with pytest.raises(exceptions.StreamError):
        sohmetrics.get_merged_stream(
            empty_stream)


def test_get_stream_data_of_merged_streams(stream_with_gaps: obspy.Stream,
                                           stream_without_gaps: obspy.Stream,
                                           empty_stream: obspy.Stream):
    # Stream with gaps
    stream_with_gaps_merged = sohmetrics.get_merged_stream(stream_with_gaps)
    stream_with_gaps_merged_data = sohmetrics.get_stream_data_of_merged_streams(
        stream_with_gaps_merged)
    expected_stream_with_gaps_merged_data = ma.array(
        [1, 2, 3, 4, 5, 6, 7], mask=[0, 0, 0, 1, 0, 0, 0])
    assert (stream_with_gaps_merged_data ==
            expected_stream_with_gaps_merged_data).all()

    # Stream without gaps
    stream_without_gaps_merged = sohmetrics.get_merged_stream(
        stream_without_gaps)
    stream_without_gaps_merged_data = sohmetrics.get_stream_data_of_merged_streams(
        stream_without_gaps_merged)
    expected_stream_without_gaps_merged_data = np.array(
        [1, 2, 3])
    assert (stream_without_gaps_merged_data ==
            expected_stream_without_gaps_merged_data).all()
    # Stream with empty trace
    with pytest.raises(exceptions.StreamError):
        sohmetrics.get_stream_data_of_merged_streams(
            empty_stream)


def test_check_timing_quality(
        list_of_streams_timing_quality: List[obspy.Stream],
        passing_threshold: float = 5.0,
        failing_threshold: float = 95.0,
        startdate: date = date(2021, 1, 1),
        enddate: date = date(2021, 1, 2),
        network: str = "QW",
        station: str = "QCC02"):
    # Timing quality daily average falls above threshold
    results = \
        sohmetrics.check_timing_quality(
            list_of_streams=list_of_streams_timing_quality,
            threshold=passing_threshold,
            startdate=startdate,
            enddate=enddate,
            network=network,
            station=station)

    assert results.passed
    assert results.details == []
    assert results.results == [20.0, 70.0, 17.0]

    # Timing quality daily average falls below threshold
    results = \
        sohmetrics.check_timing_quality(
            list_of_streams=list_of_streams_timing_quality,
            threshold=failing_threshold, startdate=startdate,
            enddate=enddate,
            network=network,
            station=station)

    assert not results.passed
    assert results.details == ['Timing quality below 95.0% on 2021-01-01',
                               'Timing quality below 95.0% on 2021-01-02',
                               'Timing quality below 95.0% on 2021-01-03']
    assert results.results == [20.0, 70.0, 17.0]


def test_check_number_of_satellites(list_of_streams: List[obspy.Stream],
                                    passing_threshold: float = 20.0,
                                    failing_threshold: float = 30.0,
                                    startdate: date = date(2021, 1, 1)):
    # Average number of satellites locked was below threshold
    results = \
        sohmetrics.check_number_of_satellites(
            list_of_streams, threshold=passing_threshold,
            startdate=startdate)
    assert results.passed
    assert results.results == [20.0, 70.0]

    # Average number of satellites locked was above threshold
    results = \
        sohmetrics.check_number_of_satellites(
            list_of_streams, threshold=failing_threshold,
            startdate=startdate)
    assert not results.passed
    assert results.results == [20.0, 70.0]


def test_check_clock_offset(list_of_streams_clock_offset: List[obspy.Stream],
                            passing_threshold: float = 1.0,
                            failing_threshold: float = 0.1,
                            startdate: date = date(2021, 1, 1),
                            ):
    # Clock offset passes
    results = sohmetrics.check_clock_offset(
        list_of_streams_clock_offset, threshold=passing_threshold,
        startdate=startdate)
    assert results.passed
    assert results.details == []
    assert results.results == [-1.0, 0.1, 1.0, 0.5]

    # Clock phase error is too high
    results = sohmetrics.check_clock_offset(
        list_of_streams_clock_offset,
        threshold=failing_threshold,
        startdate=startdate)
    # assert not results.passed
    assert results.results == [-1.0, 0.1, 1.0, 0.5]
    assert results.details == ['Average clock phase error too high on 2021-01-03',
                               'Average clock phase error too high on 2021-01-04']

    subprocess.getoutput(
        "rm -rf 'stationvalidation_output'")


def test_check_clock_locked(list_of_streams: List[obspy.Stream],
                            list_of_streams_clock_locked: List[obspy.Stream],
                            list_of_streams_clock_locked_mix:
                            List[obspy.Stream],
                            threshold: float = 2.0,
                            startdate: date = date(2021, 1, 1)):

    # Clock was unlocked more than threshold limit
    results = sohmetrics.check_clock_locked(
        list_of_streams=list_of_streams_clock_locked,
        startdate=startdate,
        threshold=threshold)
    assert not results.passed
    assert results.results == [3.0, 4.0]
    assert results.details == ['Clock unlocked 3 times on 2021-01-01. [threshold: 2.0]',
                               'Clock unlocked 4 times on 2021-01-02. [threshold: 2.0]']

    # Results had a mix of below and above threshold
    results = sohmetrics.check_clock_locked(
        list_of_streams=list_of_streams_clock_locked_mix,
        startdate=startdate,
        threshold=threshold)
    assert results.details == ['Clock unlocked 3 times on 2021-01-01. [threshold: 2.0]',
                               'Clock unlocked 4 times on 2021-01-02. [threshold: 2.0]']
    assert not results.passed

    # Clock was unlocked less than threshold limit
    results = sohmetrics.check_clock_locked(
        list_of_streams=list_of_streams,
        startdate=startdate,
        threshold=threshold)
    assert results.passed
    assert results.results == [0.0, 0.0]
