import pytest
from datetime import date
from configparser import ConfigParser


@pytest.fixture(scope="session")
def testdata() -> dict:
    config = ConfigParser()
    config.read("stationverification/data/config.ini")
    return {"data": [[0, 0, 0, 0], [11, 0, 11, 0, 12], [1, 1, 1, 1],
                     [1, 1, 0, 1], [100, 100, 100, 100], [30,
                                                          100, 30, 100]],
            "start": date(year=2021, month=1, day=1),
            "stop": date(year=2021, month=1, day=5),
            "config": config}
