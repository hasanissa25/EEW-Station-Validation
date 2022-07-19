from stationverification.utilities.generate_report import gather_stats


def test_gather_stats(gather_stats_parameters):
    smd = gather_stats(
        start=gather_stats_parameters.startdate,
        stop=gather_stats_parameters.enddate,
        snlc=gather_stats_parameters.snlc,
        metrics=gather_stats_parameters.metrics,
        ispaq_output_directory=gather_stats_parameters.ispaq_output_directory,
    )
    assert 'QW' in smd.get_networks()
    assert 'QCC02' in smd.get_stations('QW')
    assert 'pct_above_nhnm' in smd.get_metricNames()
    assert 'num_gaps' in smd.get_metricNames()
