import pytest
from datetime import date


@pytest.fixture(scope="session")
def test_date_1_digit() -> date:
    return date(2022, 1, 9)


@pytest.fixture(scope="session")
def test_date_2_digits() -> date:
    return date(2022, 1, 24)


@pytest.fixture(scope="session")
def test_date_3_digits() -> date:
    return date(2022, 4, 24)


@pytest.fixture(scope="session")
def test_date_month_2_digits() -> date:
    return date(2022, 11, 24)
