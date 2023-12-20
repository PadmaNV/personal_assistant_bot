from datetime import datetime
from datetime import timedelta
from .Contact import Contact
from .Name import Name
from .Phone import Phone
from .Birthday import Birthday
from .Contact import Contact
from .Email import Email
from datetime import datetime
import locale
import pickle


class ContactBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)

    def validate_name(self, name):
        return len(name) >= 2 and name.isalpha()

    def validate_phone_number(self, phone_number):
        return phone_number.isdigit() and len(phone_number) == 10

    def validate_birthday(self, birthday):
        try:
            datetime.strptime(birthday, '%d.%m.%Y')
            return True
        except ValueError:
            return False

    def get_valid_name(self):
        while True:
            name = input("Введіть ім'я: ")
            if self.validate_name(name):
                return name
            else:
                print("Некоректне ім'я. Ім'я повинно містити мінімум 2 букви.")

    def get_valid_phone_number(self):
        while True:
            phone_number = input("Введіть номер телефону (10 цифр): ")
            if self.validate_phone_number(phone_number):
                return phone_number
            else:
                print("Некоректний номер телефону. Будь ласка, введіть 10 цифр.")

    def get_valid_birthday(self):
        while True:
            birthday = input("Введіть день народження (формат: DD.MM.YYYY): ")
            if self.validate_birthday(birthday):
                return birthday
            else:
                print("Некоректний формат дня народження. Будь ласка, введіть у форматі DD.MM.YYYY.")

    def add_contact_interactive(self):
        name = self.get_valid_name()
        address = input("Введіть адресу (формат: країна, місто, вулиця, дом): ")
        phone_number = self.get_valid_phone_number()
        email = input("Введіть електронну пошту: ")
        birthday = self.get_valid_birthday()
        contact = Contact(name, address, phone_number, email, birthday)
        self.add_contact(contact)
        print("Контакт додано!\n")
    

    def display_contacts(self):
        for contact in self.contacts:
            print(f"Name: {contact.data['name']}\nPhone: {contact.data['phone_number']}\n{'='*30}")


    def upcoming_birthdays(self, days):
        """
        Виводить список контактів, у яких день народження відбудеться через задану кількість днів від поточної дати.
        """
        today = datetime.now().date()
        upcoming_date = today + timedelta(days=days)

        upcoming_birthdays_list = [
            contact for contact in self.contacts
            if contact.data['birthday'] and self.validate_birthday(contact.data['birthday'])
            and datetime.strptime(contact.data['birthday'], '%d.%m.%Y').date() == upcoming_date
        ]

        if upcoming_birthdays_list:
            print(f"Контакти з днями народження через {days} днів:")
            for contact in upcoming_birthdays_list:
                print(f"Name: {contact.data['name']}\nBirthday: {contact.data['birthday']}\n{'='*30}")
        else:
            print(f"На жаль, немає контактів з днями народження через {days} днів.")


    def search_contact(self, keyword):
        results = [contact for contact in self.contacts if keyword.lower() in str(contact.data.get('name', '')).lower()]
        if results:
            print(f"Результати пошуку для '{keyword}':")
            for result in results:
                print(f"Name: {result.data.get('name', '')}\nPhone: {result.data.get('phone_number', '')}\n{'='*30}")
        else:
            print(f"Такого контакту з ім'ям '{keyword}' не існує.")

        return results


    def get_valid_input(self, prompt, field):
        while True:
            user_input = input(prompt)
            field.value = user_input
            try:
                if field.is_valid():
                    return field.value
                else:
                    raise ValueError("Invalid data.")
            except ValueError as e:
                print(f"{e} {field.validation_message}")


    def get_valid_email(self):
        while True:
            email = input("Введіть електронну пошту: ")
            mail = Email(email)
            if mail.is_valid():
                return mail
            else:
                print("Некоректний формат електронної пошти. Будь ласка, введіть у правильному форматі.")

    def get_birthdays(self, days_until_birthday):
        matching_birthdays = []
        today = datetime.today().date()

        locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')

        for contact in self.contacts:
            name = contact.data.get('name', '')
            birthday = contact.data.get('birthday', '')
            
            if birthday is None or not self.validate_birthday(birthday):
                continue

            birthday_date = datetime.strptime(birthday, '%d.%m.%Y').date()
            birthday_this_year = birthday_date.replace(year=today.year)

            if birthday_this_year < today:
                next_year = birthday_this_year.year + 1
                birthday_this_year = birthday_this_year.replace(year=next_year)

            delta_days = (birthday_this_year - today).days

            if 0 <= delta_days <= days_until_birthday:
                day_of_week = birthday_this_year.strftime("%A")
                formatted_date = birthday_this_year.strftime("%d %b %Y").capitalize()
                user_info = f"{name}: {day_of_week}, {formatted_date}"
                matching_birthdays.append(user_info)

        locale.setlocale(locale.LC_TIME, '')

        return matching_birthdays
    
    def save_to_disk(self, filename="address_book.pkl"):
        contacts_data = [contact.data for contact in self.contacts]
        with open(filename, "wb") as file:
            pickle.dump(contacts_data, file)

    def load_from_disk(self, filename="address_book.pkl"):
        try:
            with open(filename, "rb") as file:
                contacts_data = pickle.load(file)
                self.contacts = [Contact(**data) for data in contacts_data]
        except FileNotFoundError:
            # If the file is not found, create an empty list
            self.contacts = []