# flake8: noqa

import pytest

from stationverification.utilities.metric_handler import metric_handler, check_metric_exists
from stationverification.utilities import exceptions


def test_check_metric_exists():
    assert check_metric_exists("num_gaps") is True
    assert check_metric_exists("does not exist") is False


def test_metric_handler(testdata: dict):
    '''
    Test the metric_handler function
    '''
    # Check with valid metric name
    result = metric_handler(
        'amplifier_saturation', testdata["data"][0],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check with invalid metric name
    with pytest.raises(exceptions.MetricHandlerError):
        metric_handler(
            'nonexisting_metric', testdata["data"][1],
            testdata["start"], testdata["config"])


def test_check_amplifier_saturation(testdata: dict):
    '''
    Test the check_amplifier_saturation
    '''
    # Check with passing data
    result = metric_handler(
        'amplifier_saturation', testdata["data"][0],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check with failing data
    result = metric_handler(
        'amplifier_saturation', testdata["data"][1],
        testdata["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['Amplifier saturation flag set on 2021-01-01',
                              'Amplifier saturation flag set on 2021-01-03', 'Amplifier saturation flag set on 2021-01-05']


def test_check_calibration_signal(testdata: dict):
    '''
    Test the check_calibration_signal
    '''
    # Check for passing result
    result = metric_handler(
        'calibration_signal', testdata["data"][0],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'calibration_signal', testdata["data"][1],
        testdata["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['Calibration signal flag set on 2021-01-01',
                              'Calibration signal flag set on 2021-01-03', 'Calibration signal flag set on 2021-01-05']


def test_check_clock_locked(testdata: dict):
    '''
    Test the check_clock_locked function
    '''
    # Check for passing result
    result = metric_handler(
        'clock_locked', testdata["data"][5],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'clock_locked', testdata["data"][0],
        testdata["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['Clock not locked with enough satelites on 2021-01-01',
                              'Clock not locked with enough satelites on 2021-01-02',
                              'Clock not locked with enough satelites on 2021-01-03',
                              'Clock not locked with enough satelites on 2021-01-04']


def test_check_dead_channel_gsn(testdata: dict):
    '''
    Test the check_dead_channel_gsn function
    '''

    # Check for passing result
    result = metric_handler(
        'dead_channel_gsn', testdata["data"][0],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'dead_channel_gsn', testdata["data"][1],
        testdata["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['Channel dead on 2021-01-01',
                              'Channel dead on 2021-01-03',
                              'Channel dead on 2021-01-05']


def test_check_dead_channel_lin(testdata: dict):
    '''
    Test the check_dead_channel_lin function
    '''

    # Check for passing result

    result = metric_handler(
        'dead_channel_lin', testdata["data"][4],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'dead_channel_lin', testdata["data"][1],
        testdata["start"], testdata["config"])
    assert result.result is False
    assert result.details == [
        'Channel too linear on 2021-01-02',
        'Channel too linear on 2021-01-04']


def test_check_digitizer_clipping(testdata: dict):
    '''
    Test the check_digitizer_clipping function
    '''

    # Check for passing result
    result = metric_handler(
        'digitizer_clipping', testdata["data"][0],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'digitizer_clipping', testdata["data"][1],
        testdata["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['Overvoltage detected on 2021-01-01',
                              'Overvoltage detected on 2021-01-03', 'Overvoltage detected on 2021-01-05']


def test_check_max_gap(testdata: dict):
    '''
    Test the check_max_gap function
    '''
    # Check for passing result
    result = metric_handler(
        'max_gap', testdata["data"][0], testdata
        ["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'max_gap', testdata["data"][1], testdata
        ["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['Max gap of 11 seconds detected on 2021-01-01',
                              'Max gap of 11 seconds detected on 2021-01-03',
                              'Max gap of 12 seconds detected on 2021-01-05']


def test_check_max_overlap(testdata: dict):
    '''
    Test the check_max_overlap function
    '''
    # Check for passing result
    result = metric_handler(
        'max_overlap', testdata["data"][0], testdata
        ["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'max_overlap', testdata["data"][1], testdata
        ["start"], testdata["config"])
    assert result.details == ['Max overlap of 11 seconds detected on 2021-01-01',
                              'Max overlap of 11 seconds detected on 2021-01-03',
                              'Max overlap of 12 seconds detected on 2021-01-05']
    assert result.result is False


def test_check_num_gaps(testdata: dict):
    '''
    Test the check_num_gaps function
    '''
    # Check with passing data
    result = metric_handler(
        'num_gaps', testdata["data"][0], testdata
        ["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check with failing data
    result = metric_handler(
        'num_gaps', testdata["data"][1], testdata
        ["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['11 gaps detected on 2021-01-01',
                              '11 gaps detected on 2021-01-03', '12 gaps detected on 2021-01-05']


def test_check_num_overlaps(testdata: dict):
    '''
    Test the check_num_overlaps function
    '''

    # Check for passing result
    result = metric_handler(
        'num_overlaps', testdata["data"][0], testdata
        ["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'num_overlaps', testdata["data"][1], testdata
        ["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['11 overlaps detected on 2021-01-01',
                              '11 overlaps detected on 2021-01-03',
                              '12 overlaps detected on 2021-01-05']


def test_check_num_spikes(testdata: dict):
    '''
    Test the check_num_spikes function
    '''

    # Check for passing result
    result = metric_handler(
        'num_spikes', testdata["data"][0], testdata
        ["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'num_spikes', testdata["data"][1], testdata
        ["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['11 spikes detected on 2021-01-01',
                              '11 spikes detected on 2021-01-01',
                              '12 spikes detected on 2021-01-05']


def test_check_pct_above_nhnm(testdata: dict):
    '''
    Test the check_pct_above_nhnm function
    '''

    # Check for passing result
    result = metric_handler(
        'pct_above_nhnm', testdata["data"][0],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'pct_above_nhnm', testdata["data"][5],
        testdata["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['65.0% noise above the New High Noise Model']


def test_check_pct_below_nlnm(testdata: dict):
    '''
    Test the check_pct_below_nlnm function
    '''

    # Check for passing result
    result = metric_handler(
        'pct_below_nlnm', testdata["data"][0],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'pct_below_nlnm', testdata["data"][5],
        testdata["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['65.0% noise below the New Low Noise Model']


def test_check_percent_availability(testdata: dict):
    '''
    Test the check_percent_availability function
    '''

    # Check for passing result
    result = metric_handler(
        'percent_availability', testdata["data"][4],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'percent_availability', testdata["data"][5],
        testdata["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['65.0% data availability']


def test_check_spikes(testdata: dict):
    '''
    Test the check_spikes function
    '''

    # Check for passing result
    result = metric_handler(
        'spikes', testdata["data"][0], testdata
        ["start"], testdata["config"])
    assert result.result is True
    assert result.details == []
    # Check for failing result
    result = metric_handler(
        'spikes', testdata["data"][1], testdata
        ["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['Spikes flag set 11 times on 2021-01-01',
                              'Spikes flag set 11 times on 2021-01-03',
                              'Spikes flag set 12 times on 2021-01-05']


def test_check_suspect_time_tag(testdata: dict):
    '''
    Test the check_suspect_time_tag function
    '''
    # Check for passing result
    result = metric_handler(
        'suspect_time_tag', testdata["data"][0],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'suspect_time_tag', testdata["data"][1],
        testdata["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['Suspect time tag flag set on 2021-01-01',
                              'Suspect time tag flag set on 2021-01-03',
                              'Suspect time tag flag set on 2021-01-05']


def test_check_telemetry_sync_error(testdata: dict):
    '''
    Test the check_telementry_sync_error function
    '''

    # Check for passing result
    result = metric_handler(
        'telemetry_sync_error', testdata["data"][0],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'telemetry_sync_error', testdata["data"][1],
        testdata["start"], testdata["config"])
    assert result.result is False
    assert result.details == ['Telemetry sync error detected on 2021-01-01',
                              'Telemetry sync error detected on 2021-01-03',
                              'Telemetry sync error detected on 2021-01-05']


def test_check_timing_quality(testdata: dict):
    '''
    Test the check_timing_quality function
    '''
    # Check for passing result
    result = metric_handler(
        'timing_quality', testdata["data"][4],
        testdata["start"], testdata["config"])
    assert result.result is True
    assert result.details == []

    # Check for failing result
    result = metric_handler(
        'timing_quality', testdata["data"][5],
        testdata["start"], testdata["config"])
    assert result.result is False
    assert result.details == [
        'Timing quality 30% on 2021-01-01', 'Timing quality 30% on 2021-01-03']
