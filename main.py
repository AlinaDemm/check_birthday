import datetime
from calendar import monthrange
from typing import List, Tuple


class Person:
    #FIXME fix def __init__(d,m,y)

    def __init__(self, n, l, day, month, year, id_):
        self.name = n
        self.last_name = l
        self.day = day
        self.month = month
        self.year = year
        self.id = id_
    # name: str
    # last_name: str
    # birthday: str


# p: Person = Person("a", "b", "c")
# p.name = "a",
# p.last_name = 'b'
# p.birthday = '3'


def helper():
    print("Input the number of command that you need:\n[1] - Help\n[2] - Add new person\n[3] - Update person's "
          "birthday\n[4] - Delete person\n[5] - Print all persons\n[6] - Print nearest birthday\n[7] - Exit")


def get_persons_birthday() -> tuple[int, int, int]:
    while True:
        try:
            persons_birthday_input = input("Please, input person's birthday date in format 'YYYY.MM.DD': ")
            persons_birthday_list: List[str] = persons_birthday_input.split('.')
            if len(persons_birthday_list) != 3:
                print("Invalid format. Try again")
                continue
            birth_year = persons_birthday_list[0]
            birth_month = persons_birthday_list[1]
            birth_day = persons_birthday_list[2]
            birth_year = int(birth_year)
            birth_month = int(birth_month)
            birth_day = int(birth_day)
            while not validate_year(birth_year, today_year):
                birth_year_input = input("Input your CORRECT birthday year")
                birth_year = int(birth_year_input)

            while not validate_month(birth_month):
                birth_month_input = input("Input your CORRECT birthday month: ")
                birth_month = int(birth_month_input)

            while not validate_day(birth_day, birth_month, birth_year):
                birth_day_input = input("Input your CORRECT birthday day:")
                birth_day = int(birth_day_input)
            return birth_year, birth_month, birth_day
        except IndexError:
            print("Invalid format. Try again")


def new_person(size: int) -> Person:
    persons_name = input("Please, input person's name: ")
    persons_last_name = input("Please, input person's last name: ")
    birth_year, birth_month, birth_day = get_persons_birthday()

    return Person(persons_name, persons_last_name, birth_year, birth_month, birth_day, size + 1)


def update_persons_birthday(persons: List[Person]):
    try:
        person_id = int(input("For update person's birthday date please input person's id: "))
        found: bool = False
        for i in range(len(persons)):
            if person_id == persons[i].id:
                birth_year, birth_month, birth_day = get_persons_birthday()
                persons[i].year = birth_year
                persons[i].month = birth_month
                persons[i].day = birth_day
                found = True
                break

        if found:
            print("Person's birthday was updated")
        else:
            print(f'No person with ID= {person_id}')
    except ValueError:
        print("Invalid person id")


def delete_person(persons: List[Person]):
    try:
        person_id = int(input("Please input person's id: "))
        found: bool = False
        for i in range(len(persons)):
            if person_id == persons[i].id:
                persons.remove(persons[i])
                found = True
                break

        if found:
            for j in range(len(persons)):
                persons[j].id = j + 1
            print("Person was deleted")
        else:
            print(f'No person with ID= {person_id}')
    except ValueError:
        print("Invalid person id")


def print_persons(persons: List[Person]) -> None:
    for p in persons:
        print(f'Id = {p.id}, Name = {p.name}, Last name = {p.last_name}, birthday = {p.year}.{p.month}.{p.day}')


def nearest_birthday(persons: List[Person]) -> Person | None:
    last_month = 12
    next_birth: Person = None
    for i in range(len(persons)):
        if today_month > persons[i].month:
            continue
        if persons[i].month <= last_month:
            if next_birth is not None:
                if persons[i].month < next_birth.month:
                    next_birth = persons[i]
                elif persons[i].month == next_birth.month:
                    if persons[i].day < next_birth.day:
                        next_birth = persons[i]
            else:
                next_birth = persons[i]

    if next_birth is None:
        next_birth: Person = persons[0]
        for person in persons:
            if person.month < next_birth.month:
                next_birth = person
            elif person.month == next_birth.month:
                if person.day < next_birth.day:
                    next_birth = person
    return next_birth


def validate_year(birth_year: int, today_year: int) -> bool:
    birth_year = int(birth_year)
    if birth_year > today_year:
        return False
    return True


def validate_month(birth_month: int) -> bool:
    birth_month = int(birth_month)
    if not 1 <= birth_month <= 12:
        return False
    return True


def validate_day(birth_day: int, birth_month: int, birth_year: int) -> bool:
    birth_day = int(birth_day)
    correct_month_days = monthrange(int(birth_year), int(birth_month))[1]
    if int(birth_day) > correct_month_days or int(birth_day) < 1:
        return False
    return True


if __name__ == '__main__':
    today = datetime.date.today()
    today_year = today.year
    today_month = today.month
    today_day = today.day

    helper()
    persons: List[Person] = []
    while True:
        action = input("Your input: ")
        if action == '1':
            helper()
        elif action == '2':
            p: Person = new_person(len(persons))
            persons.append(p)
        elif action == '3':
            update_persons_birthday(persons)
        elif action == '4':
            delete_person(persons)
        elif action == '5':
            print_persons(persons)
        elif action == '6':
            person: Person|None = nearest_birthday(persons)
            if person is not None:
                print(
                    f'The next birthday is: {person.year}.{person.month}.{person.day} (Id = {person.id}, Name = {person.name}, Last name = {person.last_name})')
        elif action == '7':
            exit()
        else:
            helper()
