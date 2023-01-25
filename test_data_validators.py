import pytest
from typing import List
from main import validate_day, validate_month, validate_year, delete_person, Person


@pytest.mark.parametrize('day,month,year,result', [(32, 12, 1997, False), (31, 5, 1998, True)])
def test_validate_day(day, month, year, result):
    assert validate_day(day, month, year) == result


@pytest.mark.parametrize('month, result', [(0, False), (13, False), (5, True)])
def test_validate_month(month, result):
    assert validate_month(month) == result


@pytest.mark.parametrize('birth_year, today_year, result', [(1999, 2008, True), (2000, 1990, False)])
def test_validate_year(birth_year, today_year, result):
    assert validate_year(birth_year, today_year) == result


@pytest.mark.parametrize('persons, person_id, result', [([], "1", False),
                                                        ([], "abf", False),
                                                        ([Person("vasily", "kovalev", 1998, 5, 31, 1)], "2", False),
                                                        ([Person("vasily", "kovalev", 1998, 5, 31, 1)], "1", True),
                                                        ])
def test_delete_person(persons, person_id, result):
    persons_len = len(persons)
    assert delete_person(persons, person_id) == result

    if result == True:
        assert (persons_len - 1) == len(persons)
