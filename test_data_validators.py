import os
import pytest
from typing import List
from main import validate_day, validate_month, validate_year, delete_person, Person, save_to_file, read_from_file


@pytest.mark.parametrize('day,month,year,result', [(32, 12, 1997, False), (29, 2, 2022, False), (31, 5, 1998, True)])
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
                                                        ([Person("alina", "demeneva", 1997, 12, 25, 1),
                                                          Person("maria", "a", 1999, 5, 5, 2),
                                                          Person("vasily", "kovalev", 1998, 5, 31, 3)], "2", True)
                                                        ])
def test_delete_person(persons, person_id, result):
    persons_len = len(persons)
    assert delete_person(persons, person_id) == result

    if result == True:
        assert (persons_len - 1) == len(persons)
        for i in range(len(persons)):
            assert persons[i].id == i + 1


def test_save_to_file():
    pe: List[Person] = [Person("vasily", "kovalev", 1998, 5, 31, 1)]
    login = "login"
    save_to_file(pe, login)

    new_persons: List[Person] = []
    read_from_file(new_persons, login)

    assert pe[0].id == new_persons[0].id
    assert pe[0].name == new_persons[0].name
    assert pe[0].last_name == new_persons[0].last_name
    assert pe[0].day == new_persons[0].day
    assert pe[0].year == new_persons[0].year
    assert pe[0].month == new_persons[0].month

    os.remove(f'{login}.txt')


def test_read_file_doesnt_exist():
    login = "login"

    new_persons: List[Person] = []
    read_from_file(new_persons, login)


def test_make_persons_and_read_file():
    pe: List[Person] = [Person("vasily", "kovalev", 1998, 5, 31, 1), Person("maria", "a", 1999, 5, 5, 2),
                        Person("alina", "demeneva", 1997, 12, 25, 3)]
    login = "login"
    save_to_file(pe, login)

    new_persons: List[Person] = []
    read_from_file(new_persons, login)
    assert len(pe) == len(new_persons)
    for i in range(0, len(pe)):
        assert pe[i].id == new_persons[i].id
        assert pe[i].name == new_persons[i].name
        assert pe[i].last_name == new_persons[i].last_name
        assert pe[i].day == new_persons[i].day
        assert pe[i].year == new_persons[i].year
        assert pe[i].month == new_persons[i].month

    os.remove(f'{login}.txt')

def test_invalid_record_in_file():
    pe: List[Person] = [Person("vasily", "kovalev", 1998, 5, 31, 1), Person("maria", "a", 1999, 5, 5, 2),
                        Person("alina", "demeneva", 1997, 12, 25, 3)]
    login = "login"
    save_to_file(pe, login)

    search_text = "Name=" + pe[1].name
    replace_text = ""

    with open(f'{login}.txt', 'r') as f:
        data = f.read()
        data = data.replace(search_text, replace_text)
    with open(f'{login}.txt', 'w') as f:
        f.write(data)

    new_persons: List[Person] = []
    read_from_file(new_persons, login)

    assert len(pe) != len(new_persons)

    pe.remove(pe[1])
    pe[1].id = 2

    for i in range(0, len(pe)):
        assert pe[i].id == new_persons[i].id
        assert pe[i].name == new_persons[i].name
        assert pe[i].last_name == new_persons[i].last_name
        assert pe[i].day == new_persons[i].day
        assert pe[i].year == new_persons[i].year
        assert pe[i].month == new_persons[i].month

    os.remove(f'{login}.txt')