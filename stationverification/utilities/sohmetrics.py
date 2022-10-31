import obspy
import logging
import subprocess
import numpy as np
import numpy.ma as ma
from datetime import date, timedelta
from typing import List, Any, Optional

from stationverification.utilities import exceptions
from stationverification.utilities.plot_timing_quality import\
    plot_timing_quality


class MetricResults(dict):
    @property
    def passed(self) -> bool:
        return self["passed"]

    @property
    def details(self) -> str:
        return self["details"]

    @property
    def results(self) -> list:
        return self["results"]


class StreamStats(dict):
    @property
    def average(self) -> float:
        return self["average"]

    @property
    def minimum(self) -> float:
        return self["minimum"]

    @property
    def maximum(self) -> float:
        return self["maximum"]


def getsohfiles(
        network: str,
        station: str,
        channel: str,
        startdate: date,
        enddate: date,
        soh_directory: str,
        location: Any = None) -> List[str]:
    '''
    Retrieves a list of the daily SOH channel files for the specified SOH
    channel

    Parameters
    ----------
    network: str
        Network Code
    station: str
        Station Code
    channel: str
        Specific SOH channel code
    startdate: date
        The first day to search for files for
    enddate: date
        The end date for the search, non-inclusive
    soh_directory: str
        The directory where the soh archive should be found

    Returns
    -------
    list
        List of files found for the specified station, SOH channel and time
        period
    '''

    files: List[str] = []
    iterdate = startdate
    if location is None:
        snlc = f'{network}.{station}.*.{channel}'
    else:
        snlc = f'{network}.{station}.{location}.{channel}'
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
        logging.warning(f'No SOH files found for {channel}')
    logging.debug(
        f'{len(files)} files found for {network}.{station}.{channel} \
            between {startdate} and {enddate}')
    return files


def get_list_of_streams_from_list_of_files(files: List[str]) -> \
        List[obspy.Stream]:
    '''
    Gets a list of files, and returns a list of streams. There will be a \
        single merged trace for each file passed.
    Each stream returned represents 1 day of data


    Parameters
    ----------
    files: List[str]
        File locations to of the Obspy stream

    Returns
    -------
    list: List[obspy.Stream]
        Merged Obspy streams from the given files
    '''
    if len(files) < 1:
        raise exceptions.StreamError(
            'Can not fetch any streams. The list of files passed to fetch \
streams from was empty')
    list_of_merged_streams = []
    # For each file, get the stream, and merge the traces
    for file in files:
        stream = obspy.read(file)
        merged_stream = get_merged_stream(stream)
        list_of_merged_streams.append(merged_stream)
    return list_of_merged_streams


def getstats(
        stream: obspy.Stream) -> StreamStats:
    '''
    Gathers statistics from a SOH miniseed stream

    Parameters
    ----------
    stream: obspy.Stream
        The obspy stream we will be retreiving the traces from
    Returns
    -------
    tuple: (float,float,float)
        (average, minimum, maximum)
    '''

    merged_stream = get_merged_stream(stream)
    merged_stream_data = get_stream_data_of_merged_streams(merged_stream)
    # Find the average, minimum and maximum
    average = float(np.average(merged_stream_data))
    minimum = float(np.min(merged_stream_data))
    maximum = float(np.max(merged_stream_data))
    logging.debug(
        f'Statistics for {stream}: average {average}, minimum {minimum},\
             maximum {maximum}')
    return StreamStats(average=average, minimum=minimum, maximum=maximum)


def get_merged_stream(stream: obspy.Stream) -> obspy.Stream:
    '''
    Merges a stream of multiple miniseed traces, into one trace

    Parameters
    ----------
    stream: Obspy Stream
        obspy stream with traces that will be merged if necessary

    Returns
    ----------
        Streams with 1 single trace of data, consisting of all the merged\
             samples
    '''
    # Merge the traces in the stream passed into one trace
    stream.merge(method=1)
    # throw an exception if the stream has no traces
    if len(stream) == 0:
        raise exceptions.StreamError(f'There were no traces found in the stream passed.\
             {stream}')
    return stream


def get_stream_data_of_merged_streams(stream: obspy.Stream) -> obspy.Trace:
    '''
    Takes a merged stream and returns its data

    Parameters
    ----------
    stream: Obspy Stream
        obspy stream with traces that is already merged

    Returns
    ----------
        1 single trace of data
    '''
    merged_stream: Any = []
    try:
        merged_stream = get_merged_stream(stream)
        return merged_stream[0].data
    except exceptions.StreamError:
        raise exceptions.StreamError(
            'There were no traces found in the stream passed')


def get_list_of_data_from_list_of_streams(list_of_streams:
                                          List[obspy.Stream]) \
        -> List[Any]:
    '''
    Takes a list of merged streams, and returns a list of stream data

    Parameters
    ----------
    list_of_streams: list of Obspy Streams

    Returns
    ----------
        a list of arrays from the stream data
    '''
    list_of_data = []
    for stream in list_of_streams:
        stream_data = get_stream_data_of_merged_streams(stream)
        list_of_data.append(stream_data)
    return list_of_data


def check_timing_quality(list_of_streams: List[obspy.Stream],
                         threshold: float,
                         startdate: date,
                         enddate: date,
                         network: str,
                         station: str,
                         location: Optional[str] = None) -> MetricResults:
    '''
    Function to check the timing quality SOH channel and ensure the daily
    averages fall above a specific threshold

    Parameters
    ----------
        list_of_streams
            List of SOH stream data to read (A stream is a set of traces /
             one merged trace)
            Channel='LCQ'
        threshold:
            Lowest allowed timing quality
        startdate:
            Start date of the validation period
        enddate:
            Start date of the validation period
        network:
            Network code for the station being validated
        station:
            Station code for the station being validated

    Returns
    -------
        bool
            Indicates if the metric passed

        string
            Text indicating the reason why the metric may have failed

        list
            List of the results for the metric
    '''
    results: Any = np.array([])
    details = []
    passed = True
    # Loop though the streams
    for stream in list_of_streams:
        # Get the stats for the stream and append the average to an np array
        stats = getstats(stream)
        results = np.append(results, round(stats.average, 2))
        # Count how many of the days have an average timing quality below the
        # threshold
    plot_timing_quality(network=network,
                        station=station,
                        startdate=startdate,
                        enddate=enddate,
                        results=results,
                        threshold=threshold,
                        location=location
                        )
    for index, value in enumerate(results):
        if value < threshold:
            passed = False
            details.append(
                f'Timing quality below {threshold}% on \
{startdate + timedelta(days=index)}')

    return MetricResults(passed=passed,
                         details=details,
                         results=results.tolist())


def check_clock_locked(
        list_of_streams: List[obspy.Stream],
        threshold: float, startdate=date) -> MetricResults:
    '''
    Check the number of times the clock is locked for a specific station.
        Each stream passed in the list_of_streams represents a day
    The first entry in the list_of_streams is the first day, which will the \
        startdate.

    Parameters
    ----------
        list_of_streams
            List of SOH stream data to read (A stream is a set of traces /
             one merged trace)
            Channel='GST'

    Returns
    -------
        bool
            Indicates if the metric passed

        string
            Text indicating the reason why the metric may have failed

        list
            List of the results for the metric
    '''
    results: Any = np.array([])
    # Loop through the streams
    for stream in list_of_streams:
        # Count how many times the clock is locked for a day
        stream_data = get_stream_data_of_merged_streams(stream)
        values = ma.array(stream_data)
        count = np.count_nonzero(values < 2)
        results = np.append(results, count)
    results = results.tolist()
    # Check each day to see if the clock is locked enough times
    passed = True
    details = []
    for index, numberOfTimesLocked in enumerate(results):
        testdate = startdate + timedelta(days=index)
        if numberOfTimesLocked > threshold:
            details.append(f'Clock unlocked {int(numberOfTimesLocked)} times on {testdate}. \
[threshold: {threshold}]')
            passed = False
    return MetricResults(passed=passed, details=details, results=results)


def check_clock_offset(list_of_streams: List[obspy.Stream],
                       threshold: float,
                       startdate: date) -> MetricResults:
    '''
    Check the average clock offset for each day.

    Parameters
    ----------
        list_of_streams
            List of SOH stream data to read (A stream is a set of traces /
             one merged trace)
            Channel='LCE'
        threshold:
            Maximum average sample clock offset from timesource
        startdate:
            Start date of the validation period
        enddate:
            Start date of the validation period
        network:
            Network code for the station being validated
        station:
            Station code for the station being validated

    Returns
    -------
    bool
        Indicates if the metric passed

    string
        Text indicating the reason why the metric may have failed

    list
        List of the results for the metric
    '''

    passed = True
    offsets = []
    details = []
    for stream in list_of_streams:
        stats = getstats(stream)
        offsets.append(stats.average)
    for index, clockPhaseError in enumerate(offsets):
        testdate = startdate + timedelta(index)
        if clockPhaseError > threshold:
            passed = False
            details.append(f'Average clock phase error too high on \
{testdate}')
    return MetricResults(passed=passed, details=details, results=offsets)


def check_number_of_satellites(
    list_of_streams: List[obspy.Stream],
        threshold: float, startdate=date) -> MetricResults:
    '''
    Checks the average number of satellites locked for each day for a station

    Parameters
    ----------
        list_of_streams
            List of SOH stream data to read (A stream is a set of traces /
             one merged trace)
            Channel='GNS'

    Returns
    -------
        bool
            Indicates if the metric passed

        string
            Text indicating the reason why the metric may have failed

        list
            List of the results for the metric
    '''

    passed = True
    details = []
    results = []

    for stream in list_of_streams:
        stats = getstats(stream)
        results.append(int(stats.average))

    for index, numberOfSatellites in enumerate(results):
        testdate = startdate + timedelta(days=index)
        if numberOfSatellites < threshold:
            passed = False
            details.append(f'Average number of GNS satellites used was {numberOfSatellites} on \
{testdate} [threshold: {threshold}]')
    return MetricResults(passed=passed, details=details, results=results)
