from typing import List
import pytest
from datetime import date
import obspy
from obspy.core.utcdatetime import UTCDateTime
import numpy as np
import numpy.ma as ma


@pytest.fixture(scope="session")
def example_files() -> List[str]:
    trace1 = obspy.Trace(data=np.array([1, 2, 3]), header={
                         "starttime": UTCDateTime('2021-01-01T00:00:00')})
    trace2 = obspy.Trace(data=np.array([5, 6, 7]), header={
                         "starttime": UTCDateTime('2021-01-01T00:00:03')})
    stream1 = obspy.Stream(traces=trace1)
    stream2 = obspy.Stream(traces=trace2)
    stream3 = obspy.Stream(traces=[trace1, trace2])
    stream3.merge(method=1)
    stream1.write("tests/sohmetrics/test_streams/stream1.mseed")
    stream2.write("tests/sohmetrics/test_streams/stream2.mseed")
    stream3.write("tests/sohmetrics/test_streams/stream3.mseed")

    return ["tests/sohmetrics/test_streams/stream1.mseed",
            "tests/sohmetrics/test_streams/stream2.mseed",
            "tests/sohmetrics/test_streams/stream3.mseed"
            ]


@pytest.fixture(scope="session")
def sohcriteria() -> dict:
    return {"network": "QW", "station": "QCC02", "channel": "LCQ",
            "startdate": date(2022, 4, 1), "enddate": date(2022, 4, 2),
            "directory": "tests/data/apollo/archive/soh", "threshold": 5.05}


@pytest.fixture(scope="session")
def stream_with_gaps() -> obspy.Stream:
    trace1 = obspy.Trace(data=np.array([1, 2, 3]), header={
                         "starttime": UTCDateTime('2021-01-01T00:00:00')})
    trace2 = obspy.Trace(data=np.array([5, 6, 7]), header={
                         "starttime": UTCDateTime('2021-01-01T00:00:04')})
    stream = obspy.Stream(traces=[trace1, trace2])
    return stream


@pytest.fixture(scope="session")
def stream_without_gaps() -> obspy.Stream:
    trace1 = obspy.Trace(data=np.array([1, 2, 3]), header={
                         "starttime": UTCDateTime('2021-01-01T00:00:00')})
    stream = obspy.Stream(traces=[trace1])
    return stream


@pytest.fixture(scope="session")
def empty_stream() -> obspy.Stream:
    trace1 = obspy.Trace(data=np.array([]))
    stream = obspy.Stream(traces=[trace1])
    return stream


@pytest.fixture(scope="session")
def list_of_streams() -> List[obspy.Stream]:
    trace1 = obspy.Trace(data=ma.array(
        [10, 20, 30, 40], mask=[0, 0, 0, 1]), header={
        "starttime": UTCDateTime('2021-01-01T00:00:00')})
    trace2 = obspy.Trace(data=np.array([60, 70, 80]), header={
                         "starttime": UTCDateTime('2021-01-01T00:00:05')})
    stream1 = obspy.Stream(traces=[trace1])
    stream2 = obspy.Stream(traces=[trace2])
    list_of_streams = []
    list_of_streams.append(stream1)
    list_of_streams.append(stream2)
    return list_of_streams


@pytest.fixture(scope="session")
def list_of_streams_timing_quality() -> List[obspy.Stream]:
    trace1 = obspy.Trace(data=ma.array(
        [10, 20, 30, 40], mask=[0, 0, 0, 1]), header={
        "starttime": UTCDateTime('2021-01-01T00:00:00')})
    trace2 = obspy.Trace(data=np.array([60, 70, 80]), header={
                         "starttime": UTCDateTime('2021-01-01T00:00:05')})
    trace3 = obspy.Trace(data=np.array([12.5, 17.5, 21]), header={
                         "starttime": UTCDateTime('2021-01-01T00:00:05')})
    stream1 = obspy.Stream(traces=[trace1])
    stream2 = obspy.Stream(traces=[trace2])
    stream3 = obspy.Stream(traces=[trace3])

    list_of_streams = []
    list_of_streams.append(stream1)
    list_of_streams.append(stream2)
    list_of_streams.append(stream3)

    return list_of_streams


@pytest.fixture(scope="session")
def list_of_streams_clock_locked() -> List[obspy.Stream]:
    trace1 = obspy.Trace(data=ma.array(
        [1, 1.5, 1.8, 30, 40], mask=[0, 0, 0, 0, 1]), header={
        "starttime": UTCDateTime('2021-01-01T00:00:00')})
    trace2 = obspy.Trace(data=np.array([1, 1.4, 1.7, 1.78, 70, 80]), header={
                         "starttime": UTCDateTime('2021-01-01T00:00:00')})
    stream1 = obspy.Stream(traces=[trace1])
    stream2 = obspy.Stream(traces=[trace2])
    list_of_streams = []
    list_of_streams.append(stream1)
    list_of_streams.append(stream2)
    return list_of_streams


@pytest.fixture(scope="session")
def list_of_streams_clock_locked_mix() -> List[obspy.Stream]:
    trace1 = obspy.Trace(data=ma.array(
        [1, 1.5, 1.7, 30, 40], mask=[0, 0, 0, 0, 1]), header={
        "starttime": UTCDateTime('2021-01-01T00:00:00')})
    trace2 = obspy.Trace(data=np.array([1, 1.4, 1.7, 1.78, 70, 80]), header={
                         "starttime": UTCDateTime('2021-01-01T00:00:00')})
    stream1 = obspy.Stream(traces=[trace1])
    stream2 = obspy.Stream(traces=[trace2])
    list_of_streams = []
    list_of_streams.append(stream1)
    list_of_streams.append(stream2)
    return list_of_streams


@pytest.fixture(scope="session")
def list_of_streams_clock_offset() -> List[obspy.Stream]:
    trace1 = obspy.Trace(data=np.array([-1]),
                         header={
                         "starttime": UTCDateTime('2021-01-01T00:00:00')})
    trace2 = obspy.Trace(data=np.array([0.1]),
                         header={
                         "starttime": UTCDateTime('2021-01-02T00:00:00')})
    trace3 = obspy.Trace(data=np.array([1]),
                         header={
                         "starttime": UTCDateTime('2021-01-03T00:00:00')})
    trace4 = obspy.Trace(data=np.array([0.5]),
                         header={
                         "starttime": UTCDateTime('2021-01-04T00:00:00')})
    stream1 = obspy.Stream(traces=[trace1])
    stream2 = obspy.Stream(traces=[trace2])
    stream3 = obspy.Stream(traces=[trace3])
    stream4 = obspy.Stream(traces=[trace4])
    list_of_streams = []
    list_of_streams.append(stream1)
    list_of_streams.append(stream2)
    list_of_streams.append(stream3)
    list_of_streams.append(stream4)

    return list_of_streams
