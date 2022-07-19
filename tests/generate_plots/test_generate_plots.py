# flake8:noqa
import subprocess
from pathlib import Path
from datetime import timedelta
from stationverification.utilities.generate_report import gather_stats
from stationverification.utilities.generate_plots import plot_metrics,\
    PlotParameters


def test_generate_plots(gather_stats_parameters):
    subprocess.getoutput(
        "rm -rf 'stationvalidation_output'")
    stationMetricData_multiple_days = gather_stats(
        snlc=gather_stats_parameters.snlc,
        start=gather_stats_parameters.startdate,
        stop=gather_stats_parameters.enddate,
        metrics=gather_stats_parameters.metrics,
        ispaq_output_directory=gather_stats_parameters.ispaq_output_directory)
    for channel in stationMetricData_multiple_days.get_channels(
        network=gather_stats_parameters.network,
        station=gather_stats_parameters.station
    ):
        plot_metrics(
            PlotParameters(network=gather_stats_parameters.network,
                           station=gather_stats_parameters.station,
                           channel=channel,
                           location=None,
                           stationMetricData=stationMetricData_multiple_days,
                           start=gather_stats_parameters.startdate,
                           stop=gather_stats_parameters.enddate)
        )
    stationMetricData_single_day = gather_stats(
        snlc=gather_stats_parameters.snlc,
        start=gather_stats_parameters.startdate,
        stop=gather_stats_parameters.startdate + timedelta(days=1),
        metrics=gather_stats_parameters.metrics,
        ispaq_output_directory=gather_stats_parameters.ispaq_output_directory)
    for channel in stationMetricData_single_day.get_channels(
        network=gather_stats_parameters.network,
        station=gather_stats_parameters.station
    ):

        plot_metrics(
            PlotParameters(network=gather_stats_parameters.network,
                           station=gather_stats_parameters.station,
                           channel=channel,
                           location=None,
                           stationMetricData=stationMetricData_single_day,
                           start=gather_stats_parameters.startdate,
                           stop=gather_stats_parameters.startdate + timedelta(days=1))
        )
    adc_count_HNE_multiple_days = Path(
        "stationvalidation_output/QW.QCC02..HNE.2022-04-01_2022-04-03.adc_count.png")
    max_gap_HNE_multiple_days = Path(
        "stationvalidation_output/QW.QCC02..HNE.2022-04-01_2022-04-03.max_gap.png")
    num_gaps_HNE_multiple_days = Path(
        "stationvalidation_output/QW.QCC02..HNE.2022-04-01_2022-04-03.num_gaps.png")
    num_overlaps_HNE_multiple_days = Path(
        "stationvalidation_output/QW.QCC02..HNE.2022-04-01_2022-04-03.num_overlaps.png")
    pct_above_nhnm_HNE_multiple_days = Path(
        "stationvalidation_output/QW.QCC02..HNE.2022-04-01_2022-04-03.pct_above_nhnm.png")
    pct_below_nlnm_HNE_multiple_days = Path(
        "stationvalidation_output/QW.QCC02..HNE.2022-04-01_2022-04-03.pct_below_nlnm.png")
    spikes_HNE_multiple_days = Path(
        "stationvalidation_output/QW.QCC02..HNE.2022-04-01_2022-04-03.spikes.png")
    adc_count_HNN_multiple_days = Path(
        "stationvalidation_output/QW.QCC02..HNN.2022-04-01_2022-04-03.adc_count.png")
    max_gap_HNN_multiple_days = Path(
        "stationvalidation_output/QW.QCC02..HNN.2022-04-01_2022-04-03.max_gap.png")
    num_gaps_HNN_multiple_days = Path(
        "stationvalidation_output/QW.QCC02..HNN.2022-04-01_2022-04-03.num_gaps.png")
    num_overlaps_HNN_multiple_days = Path(
        "stationvalidation_output/QW.QCC02..HNN.2022-04-01_2022-04-03.num_overlaps.png")
    pct_above_nhnm_HNN_multiple_days = Path(
        "stationvalidation_output/QW.QCC02..HNN.2022-04-01_2022-04-03.pct_above_nhnm.png")
    pct_below_nlnm_HNN_multiple_days = Path(
        "stationvalidation_output/QW.QCC02..HNN.2022-04-01_2022-04-03.pct_below_nlnm.png")
    spikes_HNN_multiple_days = Path(
        "stationvalidation_output/QW.QCC02..HNN.2022-04-01_2022-04-03.spikes.png")
    adc_count_HNZ_multiple_days = Path(
        "stationvalidation_output/QW.QCC02..HNZ.2022-04-01_2022-04-03.adc_count.png")
    max_gap_HNZ_multiple_days = Path(
        "stationvalidation_output/QW.QCC02..HNZ.2022-04-01_2022-04-03.max_gap.png")
    num_gaps_HNZ_multiple_days = Path(
        "stationvalidation_output/QW.QCC02..HNZ.2022-04-01_2022-04-03.num_gaps.png")
    num_overlaps_HNZ_multiple_days = Path(
        "stationvalidation_output/QW.QCC02..HNZ.2022-04-01_2022-04-03.num_overlaps.png")
    pct_above_nhnm_HNZ_multiple_days = Path(
        "stationvalidation_output/QW.QCC02..HNZ.2022-04-01_2022-04-03.pct_above_nhnm.png")
    pct_below_nlnm_HNZ_multiple_days = Path(
        "stationvalidation_output/QW.QCC02..HNZ.2022-04-01_2022-04-03.pct_below_nlnm.png")
    spikes_HNZ_multiple_days = Path(
        "stationvalidation_output/QW.QCC02..HNZ.2022-04-01_2022-04-03.spikes.png")
    adc_count_HNE_single_day = Path(
        "stationvalidation_output/QW.QCC02..HNE.2022-04-01.adc_count.png")
    max_gap_HNE_single_day = Path(
        "stationvalidation_output/QW.QCC02..HNE.2022-04-01.max_gap.png")
    num_gaps_HNE_single_day = Path(
        "stationvalidation_output/QW.QCC02..HNE.2022-04-01.num_gaps.png")
    num_overlaps_HNE_single_day = Path(
        "stationvalidation_output/QW.QCC02..HNE.2022-04-01.num_overlaps.png")
    pct_above_nhnm_HNE_single_day = Path(
        "stationvalidation_output/QW.QCC02..HNE.2022-04-01.pct_above_nhnm.png")
    pct_below_nlnm_HNE_single_day = Path(
        "stationvalidation_output/QW.QCC02..HNE.2022-04-01.pct_below_nlnm.png")
    spikes_HNE_single_day = Path(
        "stationvalidation_output/QW.QCC02..HNE.2022-04-01.spikes.png")
    adc_count_HNN_single_day = Path(
        "stationvalidation_output/QW.QCC02..HNN.2022-04-01.adc_count.png")
    max_gap_HNN_single_day = Path(
        "stationvalidation_output/QW.QCC02..HNN.2022-04-01.max_gap.png")
    num_gaps_HNN_single_day = Path(
        "stationvalidation_output/QW.QCC02..HNN.2022-04-01.num_gaps.png")
    num_overlaps_HNN_single_day = Path(
        "stationvalidation_output/QW.QCC02..HNN.2022-04-01.num_overlaps.png")
    pct_above_nhnm_HNN_single_day = Path(
        "stationvalidation_output/QW.QCC02..HNN.2022-04-01.pct_above_nhnm.png")
    pct_below_nlnm_HNN_single_day = Path(
        "stationvalidation_output/QW.QCC02..HNN.2022-04-01.pct_below_nlnm.png")
    spikes_HNN_single_day = Path(
        "stationvalidation_output/QW.QCC02..HNN.2022-04-01.spikes.png")
    adc_count_HNZ_single_day = Path(
        "stationvalidation_output/QW.QCC02..HNZ.2022-04-01.adc_count.png")
    max_gap_HNZ_single_day = Path(
        "stationvalidation_output/QW.QCC02..HNZ.2022-04-01.max_gap.png")
    num_gaps_HNZ_single_day = Path(
        "stationvalidation_output/QW.QCC02..HNZ.2022-04-01.num_gaps.png")
    num_overlaps_HNZ_single_day = Path(
        "stationvalidation_output/QW.QCC02..HNZ.2022-04-01.num_overlaps.png")
    pct_above_nhnm_HNZ_single_day = Path(
        "stationvalidation_output/QW.QCC02..HNZ.2022-04-01.pct_above_nhnm.png")
    pct_below_nlnm_HNZ_single_day = Path(
        "stationvalidation_output/QW.QCC02..HNZ.2022-04-01.pct_below_nlnm.png")
    spikes_HNZ_single_day = Path(
        "stationvalidation_output/QW.QCC02..HNZ.2022-04-01.spikes.png")
    if adc_count_HNE_multiple_days.exists() \
            and max_gap_HNE_multiple_days.exists()\
            and num_gaps_HNE_multiple_days.exists()\
            and num_overlaps_HNE_multiple_days.exists()\
            and pct_above_nhnm_HNE_multiple_days.exists()\
            and pct_below_nlnm_HNE_multiple_days.exists()\
            and spikes_HNE_multiple_days.exists() \
            and adc_count_HNN_multiple_days.exists() \
            and max_gap_HNN_multiple_days.exists()\
            and num_gaps_HNN_multiple_days.exists()\
            and num_overlaps_HNN_multiple_days.exists()\
            and pct_above_nhnm_HNN_multiple_days.exists()\
            and pct_below_nlnm_HNN_multiple_days.exists()\
            and spikes_HNN_multiple_days.exists()\
            and adc_count_HNZ_multiple_days.exists() \
            and max_gap_HNZ_multiple_days.exists()\
            and num_gaps_HNZ_multiple_days.exists()\
            and num_overlaps_HNZ_multiple_days.exists()\
            and pct_above_nhnm_HNZ_multiple_days.exists()\
            and pct_below_nlnm_HNZ_multiple_days.exists()\
            and spikes_HNZ_multiple_days.exists()\
            and adc_count_HNE_single_day.exists() \
            and max_gap_HNE_single_day.exists()\
            and num_gaps_HNE_single_day.exists()\
            and num_overlaps_HNE_single_day.exists()\
            and pct_above_nhnm_HNE_single_day.exists()\
            and pct_below_nlnm_HNE_single_day.exists()\
            and spikes_HNE_single_day.exists() \
            and adc_count_HNN_single_day.exists() \
            and max_gap_HNN_single_day.exists()\
            and num_gaps_HNN_single_day.exists()\
            and num_overlaps_HNN_single_day.exists()\
            and pct_above_nhnm_HNN_single_day.exists()\
            and pct_below_nlnm_HNN_single_day.exists()\
            and spikes_HNN_single_day.exists()\
            and adc_count_HNZ_single_day.exists() \
            and max_gap_HNZ_single_day.exists()\
            and num_gaps_HNZ_single_day.exists()\
            and num_overlaps_HNZ_single_day.exists()\
            and pct_above_nhnm_HNZ_single_day.exists()\
            and pct_below_nlnm_HNZ_single_day.exists()\
            and spikes_HNZ_single_day.exists():
        assert True
    else:
        assert False
    # subprocess.getoutput(
    #     "rm -rf 'stationvalidation_output'")
