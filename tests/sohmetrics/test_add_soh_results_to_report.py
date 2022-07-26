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
                              station="BCV13",
                              location=None,
                              startdate=date(2022, 7, 23),
                              enddate=date(2022, 7, 24),
                              soh_directory="backupData/apollo/archive/soh",
                              json_dict=json_dict_test,
                              thresholds=thresholds_test,
                              typeofinstrument="titansma",
                              miniseed_directory="backupData/apollo/archive/miniseed")


def test_add_guralp_soh_results_to_report():
    json_dict_test: Dict[str, Any] = {}
    thresholds_test = ConfigParser()
    thresholds_test.read(CONFIG)
    add_soh_results_to_report(network="QW",
                              station="BCH10",
                              location="00",
                              startdate=date(2022, 8, 14),
                              enddate=date(2022, 8, 15),
                              soh_directory="backupData/guralp/archive/soh",
                              miniseed_directory="backupData/guralp/archive/miniseed",
                              json_dict=json_dict_test,
                              thresholds=thresholds_test,
                              typeofinstrument="fortimus")
