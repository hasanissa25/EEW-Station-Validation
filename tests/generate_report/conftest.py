# flake8:noqa
import pytest
from datetime import date
from configparser import ConfigParser


class GatherStatsParameters(dict):
    @property
    def snlc(self) -> list:
        return self["snlc"]

    @property
    def startdate(self) -> bool:
        return self["startdate"]

    @property
    def enddate(self) -> str:
        return self["enddate"]

    @property
    def metrics(self) -> list:
        return self["metrics"]

    @property
    def ispaq_output_directory(self) -> list:
        return self["ispaq_output_directory"]


class ReportParameters(dict):
    @property
    def typeofinstrument(self) -> list:
        return self["typeofinstrument"]

    @property
    def network(self) -> bool:
        return self["network"]

    @property
    def station(self) -> str:
        return self["station"]

    @property
    def startdate(self) -> list:
        return self["startdate"]

    @property
    def enddate(self) -> list:
        return self["enddate"]

    @property
    def latencyFiles(self) -> list:
        return self["latencyFiles"]

    @property
    def thresholds(self) -> list:
        return self["thresholds"]

    @property
    def soharchive(self) -> list:
        return self["soharchive"]


@pytest.fixture(scope="session")
def gather_stats_parameters() -> GatherStatsParameters:
    return GatherStatsParameters(snlc="QW.QCC02.x.Hxx",
                                 startdate=date(2022, 4, 1),
                                 enddate=date(2022, 4, 4),
                                 metrics="eew_test",
                                 ispaq_output_directory="tests/data/ispaq_outputs"
                                 )


@pytest.fixture(scope="session")
def report_parameters() -> ReportParameters:
    thresholds = ConfigParser()
    thresholds.read("stationverification/data/config.ini")
    return ReportParameters(typeofinstrument="APOLLO",
                            network="QW",
                            station="QCC02",
                            startdate=date(2022, 4, 1),
                            enddate=date(2022, 4, 2),
                            latencyFiles="tests/latency/test_data/apollo/archive/latency",
                            soharchive="tests/data/apollo/archive/soh",
                            thresholds=thresholds
                            )
