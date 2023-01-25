import datetime
from calendar import monthrange
from typing import List, Tuple
import hashlib


class Person:

    def __init__(self, name: str, last_name: str, year: int, month: int, day: int, id_: int):
        self.name = name
        self.last_name = last_name
        self.year = year
        self.month = month
        self.day = day
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


def ask_login_and_password() -> str:
    while True:
        try:
            user_login: str = input("Please, input your login, or print 1 to make new user, or 'exit' to exit: ")
            if user_login == "exit":
                exit()
            elif user_login == "1":
                user_login: str = input("Please, create your login: ")
                if user_login != "":
                    user_password: str = input("Please, create your password: ")
                    if user_password != "":
                        hash_password = hashlib.md5(user_password.encode('utf-8')).hexdigest()

                        try:
                            open(f'{user_login}.txt', 'x')
                            with open('users.txt', 'a') as f:
                                f.write(f'login={user_login},password={hash_password}\n')
                            return user_login
                        except FileExistsError:
                            print("Error! This login has already exist")
            else:
                with open('users.txt', 'r') as f:
                    for line in f:
                        if user_login in line:
                            user_password: str = input("Please, input your password: ")
                            hash_password = hashlib.md5(user_password.encode('utf-8')).hexdigest()
                            if user_login and hash_password in line:
                                return user_login
                            else:
                                print("Invalid password!")
        except ValueError:
            print("Invalid login or password, try again, or make new user")




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
    persons_name, persons_last_name = input("Please, input your full name: ").split(" ")
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


def recalculate_ids(persons: List[Person]):
    for j in range(len(persons)):
        persons[j].id = j + 1


def delete_person(persons: List[Person], person_id: str) -> bool:
    try:
        person_id = int(person_id)
        found: bool = False
        for i in range(len(persons)):
            if person_id == persons[i].id:
                persons.remove(persons[i])
                found = True
                break

        if found:
            recalculate_ids(persons)
            return True
        else:
            return False
    except ValueError:
        return False


def print_persons(persons: List[Person]) -> None:
    for p in persons:
        print(f'Id = {p.id}, Name = {p.name}, Last name = {p.last_name}, birthday = {p.year}.{p.month}.{p.day}')


def nearest_birthday(persons: List[Person]) -> Person:
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


def read_from_file(persons: List[Person], user_login):
    error_found: bool = False
    try:
        with open(f'{user_login}.txt', 'r') as f:
            for line in f:
                try:
                    line = line[:-1]
                    person_data: List[str] = line.split(',')
                    person_id: int = int(person_data[0].split("=")[1])
                    person_name: str = person_data[1].split("=")[1]
                    person_lastname: str = person_data[2].split("=")[1]
                    person_full_birthday = person_data[3].split("=")[1]
                    person_year: int = int(person_full_birthday.split(".")[0])
                    person_month: int = int(person_full_birthday.split(".")[1])
                    person_day: int = int(person_full_birthday.split(".")[2])
                    p: Person = Person(person_name, person_lastname, person_year, person_month, person_day, person_id)
                    persons.append(p)
                except (IndexError, ValueError) as e:
                    error_found = True
                    print("ERROR!", e)

        if error_found:
            recalculate_ids(persons)
            save_to_file(persons, user_login)
    except FileNotFoundError as e:
        print("ERROR!", e)


def save_to_file(persons: List[Person], user_login):
    with open(f'{user_login}.txt', 'w') as f:
        for p in persons:
            f.write(f'Id={p.id},Name={p.name},Last name={p.last_name},birthday={p.year}.{p.month}.{p.day}\n')


if __name__ == '__main__':
    persons: List[Person] = []
    user_login = ask_login_and_password()
    read_from_file(persons, user_login)
    today = datetime.date.today()
    today_year = today.year
    today_month = today.month
    today_day = today.day


    helper()
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
            person_id = input("Please input person's id: ")
            result: bool = delete_person(persons, person_id)
            if result:
                print(f'Person with ID {person_id} has been deleted')
            else:
                print(f'No person with ID= {person_id} or ID is invalid')
        elif action == '5':
            print_persons(persons)
        elif action == '6':
            person: Person = nearest_birthday(persons)
            if person is not None:
                print(
                    f'The next birthday is: {person.year}.{person.month}.{person.day} (Id = {person.id}, Name = {person.name}, Last name = {person.last_name})')
        elif action == '7':
            save_to_file(persons, user_login)
            exit()
        else:
            helper()
