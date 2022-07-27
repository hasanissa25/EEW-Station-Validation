# flake8:noqa
import subprocess
from pathlib import Path
from stationverification.utilities.generate_report import gather_stats, report
from stationverification.utilities.generate_latency_results\
    import generate_latency_results


def test_report(gather_stats_parameters, report_parameters):
    subprocess.getoutput(
        "rm -rf stationvalidation_output")
    stationmetricdata = gather_stats(
        start=gather_stats_parameters.startdate,
        stop=gather_stats_parameters.enddate,
        snlc=gather_stats_parameters.snlc,
        metrics=gather_stats_parameters.metrics,
        ispaq_output_directory=gather_stats_parameters.ispaq_output_directory,
    )
    combined_latency_dataframe_for_all_days = \
        generate_latency_results(typeofinstrument=report_parameters.typeofinstrument,
                                 network=report_parameters.network,
                                 station=report_parameters.station,
                                 startdate=report_parameters.startdate,
                                 enddate=report_parameters.enddate,
                                 path=report_parameters.latencyFiles,
                                 timely_threshold=report_parameters.thresholds.getfloat(
                                     'thresholds', 'data_timeliness', fallback=3))
    report(combined_latency_dataframe_for_all_days=combined_latency_dataframe_for_all_days,
           typeofinstrument=report_parameters.typeofinstrument,
           network=report_parameters.network,
           station=report_parameters.station,
           stationmetricdata=stationmetricdata,
           start=report_parameters.startdate,
           end=report_parameters.enddate,
           thresholds=report_parameters.thresholds,
           soharchive=report_parameters.soharchive)

    json_report = "stationvalidation_output/QW.QCC02...2022-04-01.validation_results.json"
    json_report_path = Path(json_report)
    if json_report_path.exists():
        assert True
    else:
        assert False
