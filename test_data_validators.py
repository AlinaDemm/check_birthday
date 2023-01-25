import pytest
from main import validate_day


def test_create_bins_db():
    assert validate_day(32, 12, 1998) == False
