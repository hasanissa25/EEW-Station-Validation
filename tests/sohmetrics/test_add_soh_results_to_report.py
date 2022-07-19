# flake8: noqa

from datetime import date

from configparser import ConfigParser
from typing import Any, Dict

from stationverification.utilities.add_soh_results_to_report import add_soh_results_to_report
from stationverification import CONFIG


def test_add_soh_results_to_report():
    json_dict_test: Dict[str, Any] = {}
    thresholds_test = ConfigParser()
    thresholds_test.read(CONFIG)
    add_soh_results_to_report(network="QW",
                              station="QCC02",
                              location=None,
                              startdate=date(2022, 4, 1),
                              enddate=date(2022, 4, 2),
                              directory="tests/data/apollo/archive/soh",
                              json_dict=json_dict_test,
                              thresholds=thresholds_test,
                              typeofinstrument="")
