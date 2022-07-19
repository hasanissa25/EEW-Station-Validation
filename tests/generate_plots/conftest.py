# flake8:noqa
import pytest
from datetime import date


class GatherStatsParameters(dict):
    @property
    def snlc(self) -> list:
        return self["snlc"]

    @property
    def network(self) -> list:
        return self["network"]

    @property
    def station(self) -> list:
        return self["station"]

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


@pytest.fixture(scope="session")
def gather_stats_parameters() -> GatherStatsParameters:
    return GatherStatsParameters(snlc="QW.QCC02.x.Hxx",
                                 network="QW",
                                 station="QCC02",
                                 startdate=date(2022, 4, 1),
                                 enddate=date(2022, 4, 4),
                                 metrics="eew_test",
                                 ispaq_output_directory="tests/data/ispaq_outputs"
                                 )
