'''
This module is used to check metric values against thresholds and assign them
a passing or failing grade

Functions
---------
metric_handler:
    Given a metric name and a list of values, passes the values to the correct
    function for validation

check_num_gap:
    Check the values for the num_gaps metric

check_amplifier_saturation:
    Check the values for the amplifier_saturation metric

check_calibration_signal
    Check the values for the calibration_signal metric

check_suspect_time_tag
    Check the values for the suspect_time_tag metric

check_timing_quality
    Check the values for the timing_quality metric

check_digitizer_clipping
    Check the values for the num_gap metric

check_max_gap
    Check the values for the max_gap metric

check_num_overlaps
    Check the values for the num_overlaps metric

check_max_overlaps
    Check the values for the max_overlaps metric

check_num_spikes
    Check the values for the num_spikes metric

check_spikes
    Check the values for the check_spikes metric

check_dead_channel_lin
    Check the values for the dead_channel_lin metric

check_dead_channel_gsn
    Check the values for the dead_channel_gsn metric

check_pct_above_nhnm
    Check the values for the pct_above_nhnm metric

check_pct_below_nlnm
    Check the values for the pct_below_nlnm metric

check_percent_availability
    Check the values for the percent_availability metric

check_clock_locked
    Check the values for the clock_locked metric

check_telemetry_sync_error
    Check the values for the telemetry_sync_error metric

'''
from datetime import date, timedelta
from configparser import ConfigParser
import logging
from typing import List

from stationverification.utilities import exceptions


class MetricResults(dict):
    @property
    def result(self) -> bool:
        return self["result"]

    @property
    def details(self) -> str:
        return self["details"]


def check_metric_exists(metric: str) -> bool:
    list_of_available_metrics = [
        'num_gaps',
        'amplifier_saturation',
        'calibration_signal',
        'suspect_time_tag',
        'timing_quality',
        'digitizer_clipping',
        'max_gap',
        'num_overlaps',
        'max_overlap',
        'num_spikes',
        'spikes',
        'dead_channel_gsn',
        'dead_channel_lin',
        'pct_above_nhnm',
        'pct_below_nlnm',
        'percent_availability',
        'clock_locked',
        'telemetry_sync_error',
    ]
    #  Grab the right function name from the switcher. If no function exists
    # for the metric, then lambda should return a blank string
    if metric not in list_of_available_metrics:
        return False
    else:
        return True

# Function that determins what metric is being checked and then passes
# the data to the correct function. Each of these functions should return a
# string of either "Passed!" or "Failed!" with some explaination of why it
# failed.


def metric_handler(
    metric: str,
    values: List[float],
    start: date,
    thresholds: ConfigParser
) -> MetricResults:
    '''
    This function determines what check_ function to call when given the name
    of a metric

    Parameters
    ----------
    metric: str
        The name of the metric to be tested
    values: list
        A list of the values to be checked for the specified metric
    start: date
        The start date of the testing period. This is used for some metrics to
        provide a date of failure
    thresholds: ConfigParser
        ConfigParser object containing threshold settings

    Returns
    -------
    bool:
        True or False indicating whether the station passed for this metric
    str:
        If the station failed the test, some detailed about why
    '''
    # Switcher dictionary containing the function references for the different
    # metrics
    switcher = {
        'num_gaps': check_num_gaps,
        'amplifier_saturation':  check_amplifier_saturation,
        'calibration_signal': check_calibration_signal,
        'suspect_time_tag': check_suspect_time_tag,
        'timing_quality': check_timing_quality,
        'digitizer_clipping': check_digitizer_clipping,
        'max_gap': check_max_gap,
        'num_overlaps': check_num_overlaps,
        'max_overlap': check_max_overlap,
        'num_spikes': check_num_spikes,
        'spikes': check_spikes,
        'dead_channel_gsn': check_dead_channel_gsn,
        'dead_channel_lin': check_dead_channel_lin,
        'pct_above_nhnm': check_pct_above_nhnm,
        'pct_below_nlnm': check_pct_below_nlnm,
        'percent_availability': check_percent_availability,
        'clock_locked': check_clock_locked,
        'telemetry_sync_error': check_telemetry_sync_error
    }

    #  Grab the right function name from the switcher. If no function exists
    # for the metric, then lambda should return a blank string
    func = switcher.get(metric)
    if func is None:
        logging.info(f'Function for metric "{metric}" was not found')
        raise exceptions.MetricHandlerError(
            'The name of the metric to be tested is incorrect or not found.')
    else:
        result = func(values, start, thresholds.getfloat(
            'thresholds', metric, fallback=0))
        return result


# There should be no gaps. Any value that isn't 0 is a fail
def check_num_gaps(
    gaps: List[float],
    start: date,
    limit: float
) -> MetricResults:
    '''
    Check that the number of gaps for each day in the test period was not
    greater than the defined threshold

    Parameters
    ----------
    gaps: list
        The values returned by ISPAQ for each day for the num_gaps metric
    start: date
        The start date of the test period.
    limit: float
        Threshold value as defined in the metric threshold preference file

    Returns
    -------
    bool:
        True or False indicating whether the station passed for this metric
    str:
        If failed, the number of gaps found on the first day that exceeded the
        threshold
    '''
    result = True
    details = []
    for index, gap in enumerate(gaps):
        if gap > limit:
            result = False
            details.append(
                f'{gap} gaps detected on {start + timedelta(days=index)}')
    return MetricResults(result=result, details=details)


# This flag is meant to signify that the preamplifier is being overridden,
# but exact meaning can vary by datalogger.
# Currently unsure if Centaurs set this flag. If the datalogger doesn't set \
# this flag, potential for a false "Passed!"
def check_amplifier_saturation(
    amplifier_saturation: List[float],
    start: date,
    limit: float
) -> MetricResults:
    '''
    Checks if the amplifier_saturation flag was set for any day, which could
    indicate that the preamplifier is being overridden

    Parameters
    ----------
    amplifier_satiration: list
        The values returned by ISPAQ for each day for the amplifier_saturation
        metric
    start: date
        The start date of the test period. Used to determine the first date
        that the amplifier_saturation flag was set
    limit: float
        Threshold value as defined in the metric threshold preference file.
        Should always be 0

    Returns
    -------
    bool:
        True or False indicating whether the station passed for this metric
    str:
        If failed, the first date that the amplifier_saturation flag was set
    '''
    result = True
    details = []
    for index, value in enumerate(amplifier_saturation):
        if not int(value) <= limit:
            result = False
            details.append(f'Amplifier saturation flag set on \
{start + timedelta(days=index)}')
    return MetricResults(result=result, details=details)


# This flag is set when a calibration is performed. Any value besides 0 is a
# fail. Centaurs set this flag, but not all dataloggers do
def check_calibration_signal(
    calibration_signal: List[float],
    start: date,
    limit: float
) -> MetricResults:
    '''
    Checks if the calibration_signal flag was set for any day, which would
    indicate that a calibration was performed on the insturmentation during
    the test period

    Parameters
    ----------
    calibration_signal: list
        The values returned by ISPAQ for each day for the amplifier_saturation
        metric
    start: date
        The start date of the test period. Used to determine the first date
        that the calibration_signal flag was set
    limit: float
        Threshold value as defined in the metric threshold preference file.
        Should be 0

    Returns
    -------
    bool:
        True or False indicating whether the station passed for this metric
    str:
        If failed, the first date that the calibration_signal flag was set
    '''
    result = True
    details = []
    for index, value in enumerate(calibration_signal):
        if not int(value) <= limit:
            result = False
            details.append(f'Calibration signal flag set on \
{start + timedelta(days=index)}')
    return MetricResults(result=result, details=details)


# This flag is set when timing quality has fallen below a datalogger-specific
# threshold.
# I tried running this for a day that I knew timing quality would
# be bad (during initial PTP testing), but the flag wasn't set. Assuming that
# this flag is not set by Centaurs, so may be a false "Passed!"
def check_suspect_time_tag(
    suspect_time_tag: List[float],
    start: date,
    limit: float
) -> MetricResults:
    '''
    Checks if the suspect_time_tag flag was set which happens when timing
    quality falls below a datalogger-specific threshold

    Parameters
    ----------
    suspect_time_tag: list
        The values returned by ISPAQ for each day for the suspect_time_tag
        metric
    start: date
        The start date of the test period. Used to determine the first date
        that the suspect_time_tag flag was set
    limit: float
        Threshold value as defined in the metric threshold preference file.
        Should be 0

    Returns
    -------
    bool:
        True or False indicating whether the station passed for this metric
    str:
        If failed, the first date that the suspect_time_tag flag was set
    '''
    result = True
    details = []
    for index, value in enumerate(suspect_time_tag):
        if not int(value) <= limit:
            result = False
            details.append(f'Suspect time tag flag set on \
{start + timedelta(days=index)}')
    return MetricResults(result=result, details=details)


# This metric is the daily average of the timing_quality values stored in the
# miniseed file.
# This metric has been returning "null" values for some reason,
# so false "Failed!" is expected.
def check_timing_quality(
    timing_quality: List[float],
    start: date,
    limit: float
) -> MetricResults:
    '''
    Checks the timing_quality value for each day is above a threshold

    Parameters
    ----------
    timing_quality: list
        The values returned by ISPAQ for each day for the timing_quality
        metric
    start: date
        The start date of the test period. Used to determine the first date
        that the amplifier_saturation flag was set
    limit: float
        Threshold value as defined in the metric threshold preference file.

    Returns
    -------
    bool:
        True or False indicating whether the station passed for this metric
    str:
        If failed, the timing quality value and date that it failed
    '''
    result = True
    details = []
    for index, value in enumerate(timing_quality):
        if value < limit:
            result = False
            details.append(f'Timing quality {value}% on \
{start + timedelta(days=index)}')
    return MetricResults(result=result, details=details)


# Any value besides 0 indicates that the input voltage exceeded the maximum
# range of the ADC.
# Unsure if this flag is being set by the Centaur, may
# return false "Passed!"
def check_digitizer_clipping(
    digitizer_clipping: List[float],
    start: date,
    limit: float
) -> MetricResults:
    '''
    Checks for the digitizer_clipping flag in waveform data which could
    indicate that the supply voltage exceeded the maximum range of the ADC

    Parameters
    ----------
    digitizer_clipping: list
        The values returned by ISPAQ for each day for the digitizer_clipping
        metric
    start: date
        The start date of the test period. Used to determine the first date
        that the digitizer_clipping flag was set
    limit: float
        Threshold value as defined in the metric threshold preference file.
        Should be 0

    Returns
    -------
    bool:
        True or False indicating whether the station passed for this metric
    str:
        If failed, the first date that the digitizer_clipping flag was set
    '''
    result = True
    details = []
    for index, value in enumerate(digitizer_clipping):
        if not value <= limit:
            result = False
            details.append(f'Overvoltage detected on \
{start + timedelta(days=index)}')
    return MetricResults(result=result, details=details)

# This metric records the longest gap in seconds. There should be no gaps, so
# any values above 0 are considered a Fail


def check_max_gap(
    max_gap: List[float],
    start: date,
    limit: float
) -> MetricResults:
    '''
    Checks the length in seconds of the largest gap in data across the entire
    testing period and compares it to the defined limit

    Parameters
    ----------
    max_gap: list
        The values returned by ISPAQ for each day for the max_gap metric
        Units: Seconds
    start: date
        The start date of the test period. Used to determine the date that the
        max_gap occured on
    limit: float
        Threshold value as defined in the metric threshold preference file.

    Returns
    -------
    bool:
        True or False indicating whether the station passed for this metric
    str:
        If failed, the size of the largest gap and the date that it appeared
    '''
    result = True
    details = []
    for index, value in enumerate(max_gap):
        if not value <= limit:
            result = False
            details.append(f'Max gap of {value} seconds detected on \
{start + timedelta(days=index)}')
    return MetricResults(result=result, details=details)


# This metric counts the number of overlaps. There should be no overlaps, so
# values above 0 are considered a fail
def check_num_overlaps(
    num_overlaps: List[float],
    start: date,
    limit: float
) -> MetricResults:
    '''
    Checks the total number of overlaps during the testing period

    Parameters
    ----------
    num_overlaps: list
        The values returned by ISPAQ for each day for the num_overlaps
        metric
    start: date
        The start date of the test period.
    limit: float
        Threshold value as defined in the metric threshold preference file

    Returns
    -------
    bool:
        True or False indicating whether the station passed for this metric
    str:
        If failed, the total number of overlaps detected
    '''
    result = True
    details = []
    for index, value in enumerate(num_overlaps):
        if value > limit:
            result = False
            details.append(f'{value} overlaps detected on \
{start + timedelta(days=index)}')
    return MetricResults(result=result, details=details)


# This metric records the duration of the longest overlap in seconds. There
# should be no overlaps, so values above 0 are Fails.
def check_max_overlap(
    max_overlap: List[float],
    start: date,
    limit: float
) -> MetricResults:
    '''
    Checks the length in seconds of the largest overlap in the data during
    the testing period and compares it to the defined limit

    Parameters
    ----------
    max_overlap: list
        A list containing length of the largest gaps for each day, as returned
        by ISPAQ
    start: date
        The start date of the test period, used to determine what date the
        largest overlap occured on
    limit: float
        Threshold value as defined in the metric threshold preference file

    Returns
    -------
    bool:
        True or False indicating whether the station passed for this metric
    str:
        If failed, the size and date of the largest overlap
    '''
    result = True
    details = []
    for index, value in enumerate(max_overlap):
        if not value <= limit:
            result = False
            details.append(f"Max overlap of {value} seconds detected on \
{start + timedelta(days=index)}")
    else:
        return MetricResults(result=result, details=details)


# This metric detects spikes using a Median Absolute Deviation approach. There
# should be no spikes, so any value above 0 is a fail. This only works for
# High Gain channels, and will be skipped by ISPAQ for any other channel.
def check_num_spikes(
    num_spikes: List[float],
    start: date,
    limit: float
) -> MetricResults:
    '''
    Detects the number of spikes for High Gain channels using a Median
    Absolute Deviation method and compares it to the defines limit

    Parameters
    ----------
    num_spikes: list
        The values returned by ISPAQ for each day for the num_spikes
        metric
    start: date
        The start date of the test period. Not used for this function, only
        included to keep the metric_handler function consistant
    limit: float
        Threshold value as defined in the metric threshold preference file

    Returns
    -------
    bool:
        True or False indicating whether the station passed for this metric
    str:
        If failed, the total number of spikes detected
    '''
    result = True
    details = []
    for index, value in enumerate(num_spikes):
        if not value <= limit:
            result = False
            details.append(f"{int(value)} spikes detected on \
{start + timedelta(days=num_spikes.index(value))}")
    else:
        return MetricResults(result=result, details=details)


# This metric checks how many times the data quality flag is set to 1,
# indicating short-duration spikes.
# I observed that this flag was not set for
# a station on a day when the "num_spikes" metric returned a value of 3.
# Assuming this flag isn't being set by Centaurs, expected false "Passed!"
def check_spikes(
    spikes: List[float],
    start: date,
    limit: float
) -> MetricResults:
    '''
    Checks the number of times that the spikes flag is set in the data and
    compares it to the defined threshold

    Parameters
    ----------
   spikes: list
        The values returned by ISPAQ for each day for the spikes metric
    start: date
        The start date of the test period. Used to determine the first date
        that the spikes flag was set
    limit: float
        Threshold value as defined in the metric threshold preference file

    Returns
    -------
    bool:
        True or False indicating whether the station passed for this metric
    str:
        If failed,  the first date that the spikes flag was set
    '''
    result = True
    details = []
    for index, value in enumerate(spikes):
        if value > limit:
            result = False
            details.append(f"Spikes flag set {value} times on \
{start + timedelta(days=index)}")
    return MetricResults(result=result, details=details)


# This metric returns 1 when a full day's corrected PSD values are 5dB below
# the NLNM line, indicating a dead channel
def check_dead_channel_gsn(
    dead_channel_gsn: List[float],
    start: date,
    limit: float
) -> MetricResults:
    '''
    Checks if the dead_channel_gsn flag was set, which occurs when the median
    probability value of a day’s worth of instrument-corrected PSD values are
    5 dB below the low noise line, indicating a dead channel

    Parameters
    ----------
    dead_channel_gsn: list
        The values returned by ISPAQ for each day for the dead_channel_gsn
        metric
    start: date
        The start date of the test period. Used to determine the first date
        that the channel died
    limit: float
        Threshold value as defined in the metric threshold preference file.
        Should be 0

    Returns
    -------
    bool:
        True or False indicating whether the station passed for this metric
    str:
        If failed, the date that the channel first appeared dead
    '''
    result = True
    details = []
    for index, value in enumerate(dead_channel_gsn):
        if not value <= limit:
            result = False
            details.append(f"Channel dead on \
{start + timedelta(days=index)}")
    return MetricResults(result=result, details=details)


# This metric determines how linear the mean of PSD values are for the channel.
# Any value below 3 indicates a dead channel. Only works for High Gain channels
def check_dead_channel_lin(
    dead_channel_lin: List[float],
    start: date,
    limit: float
) -> MetricResults:
    '''
    Fits a High Gain channel's PSD mean curve to a linear curve and compares
    the standard deviation of the residuals to the defined limit

    Parameters
    ----------
    dead_channel_lin: list
        The values returned by ISPAQ for each day for the dead_channel_lin
        metric
    start: date
        The start date of the test period. Used to determine the first date
        that the channel died
    limit: float
        Threshold value as defined in the metric threshold preference file

    Returns
    -------
    bool:
        True or False indicating whether the station passed for this metric
    str:
        If failed, the date that the channel first appeared dead
    '''
    result = True
    details = []
    for index, value in enumerate(dead_channel_lin):
        if not value >= limit:
            result = False
            details.append(f'Channel too linear on \
{start + timedelta(days=index)}')
    return MetricResults(result=result, details=details)


# Returns the percentage of corrected PSD values that fall above the NHNM. For
# a 0.25g channel, this should be very low (<5%).
# For a channel set to 2g or 4g this will probably return a false "Failed!"
def check_pct_above_nhnm(
    pct_above_nhnm: List[float],
    start: date,
    limit: float
) -> MetricResults:
    '''
    Checks the percentage of PDF values that are above the New High Nosie
    Model and compares it to the defined limit

    Parameters
    ----------
    pct_above_nhnm: list
        The values returned by ISPAQ for each day for the pct_above_nhnm
        metric
    start: date
        The start date of the test period. Not used by this function, only
        included to keep the metric_handler function consistant
    limit: float
        Threshold value as defined in the metric threshold preference file

    Returns
    -------
    bool:
        True or False indicating whether the station passed for this metric
    str:
        If failed, the percentage of PDF values above the NHNM
    '''
    average = sum(pct_above_nhnm)/float(len(pct_above_nhnm))
    result = True
    details = []
    if not average <= limit:
        result = False
        details.append(f"{average}% noise above \
the New High Noise Model")
    return MetricResults(result=result, details=details)


# Checks the percentage of corrected PSD values that fall below the NLNM.
# Should be 0%
def check_pct_below_nlnm(
    pct_below_nlnm: List[float],
    start: date,
    limit: float
) -> MetricResults:
    '''
    Checks the percentage of PDF values that are below the New Low Nosie Model
    and compares it to the defined limit

    Parameters
    ----------
    pct_below_nlnm: list
        The values returned by ISPAQ for each day for the pct_below_nlnm
        metric
    start: date
        The start date of the test period. Not used by this function, only
        included to keep the metric_handler function consistant
    limit: float
        Threshold value as defined in the metric threshold preference file

    Returns
    -------
    bool:
        True or False indicating whether the station passed for this metric
    str:
        If failed, the percentage of PDF values below the NLNM
    '''

    average = sum(pct_below_nlnm)/float(len(pct_below_nlnm))
    result = True
    details = []
    if not average <= limit:
        result = False
        details.append(f"{average}% noise below \
the New Low Noise Model")
    return MetricResults(result=result, details=details)


# The percentage of available data for the test period should be very high
def check_percent_availability(
    percent_availability: List[float],
    start: date,
    limit: float
) -> MetricResults:
    '''
    Checks the percentage of data that is available for the time series and
    compares it to the defined limit

    Parameters
    ----------
    percent_availability: list
        The values returned by ISPAQ for each day for the percent_availability
        metric
    start: date
        The start date of the test period. Not used by this function, only
        included to keep the metric_handler function consistant
    limit: float
        Threshold value as defined in the metric threshold preference file

    Returns
    -------
    bool:
        True or False indicating whether the station passed for this metric
    str:
        If failed, the percentage of data that was available
    '''

    average = sum(percent_availability)/float(len(percent_availability))
    result = True
    details = []
    if not average >= limit:
        result = False
        details.append(f"{average}% data \
availability")
    return MetricResults(result=result, details=details)


# Counts the number of times the "clock_locked" flag has been set to 1, which
# indicates that the GPS is locked with enough satellites.
# May return a false fail if the datalogger does not set this flag.
def check_clock_locked(
    clock_locked: List[float],
    start: date,
    limit: float
) -> MetricResults:
    '''
    Checks the number of times that the clock_locked flag is set in the data
    and compares it to the defined limit

    Parameters
    ----------
    clock_locked: list
        The values returned by ISPAQ for each day for the clock_locked
        metric
    start: date
        The start date of the test period. Used to return the first date that
        this flag is not set
    limit: float
        Threshold value as defined in the metric threshold preference file

    Returns
    -------
    bool:
        True or False indicating whether the station passed for this metric
    str:
        If failed, the first date when this flag was not set not set
    '''
    result = True
    details = []
    for index, value in enumerate(clock_locked):
        if not value >= limit:
            result = False
            details.append(f"Clock not locked with enough satelites on \
{start + timedelta(days=index)}")
    return MetricResults(result=result, details=details)

# Counts the number of times the data quality flag is set from 0 to 1,
# indicating data droppouts.
# May returns a false pass if the acquisition system does not set this flag


def check_telemetry_sync_error(
    telemetry_sync_error: List[float],
    start: date,
    limit: float
) -> MetricResults:
    '''
    Checks the number of times that data gaps have occured due to telemetry
    syncronization error, and compares it to the defined limit

    Parameters
    ----------
    telemetry_sync_error: list
        The values returned by ISPAQ for each day for the telemetry_sync_error
        metric
    start: date
        The start date of the test period. Used to determine what day the
        first telemetty syncronization error was detected
    limit: float
        Threshold value as defined in the metric threshold preference file

    Returns
    -------
    bool:
        True or False indicating whether the station passed for this metric
    str:
        If failed, the date of the first telemetry sync error
    '''
    result = True
    details = []
    for index, value in enumerate(telemetry_sync_error):
        if not value <= limit:
            result = False
            details.append(f"Telemetry sync error detected on \
{start + timedelta(days=index)}")
    return MetricResults(result=result, details=details)
