from .Name import Name
from .Phone import Phone
from .Birthday import Birthday
from .Contact import Contact
from .Email import Email
from datetime import datetime
import locale


class ContactBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)

    def display_contacts(self):
        for contact in self.contacts:
            print(f"Name: {contact.name}\nPhone: {contact.phone_number}\n{'='*30}")

    def search_contact(self, keyword):
        results = [contact for contact in self.contacts if keyword.lower() in str(contact.name.value).lower()]

        if results:
            print(f"Результати пошуку для '{keyword}':")
            for result in results:
                print(f"Name: {result.name}\nPhone: {result.phone_number}\n{'='*30}")
        else:
            print(f"Такого контакту з ім'ям '{keyword}' не існує.")

        return results

    def add_contact_interactive(self):
        name = self.get_valid_input("Введіть ім'я: ", Name(''))
        address = input("Введіть адресу (формат: країна, місто, вулиця, дом): ")
        phone_number = self.get_valid_input("Введіть номер телефону (10 цифр): ", Phone(''))
        email = input("Введіть електронну пошту: ")
        birthday = self.get_valid_input("Введіть день народження (формат: DD.MM.YYYY): ", Birthday(''))

        contact = Contact(name, address, phone_number, email, birthday)
        self.add_contact(contact)
        print("Контакт додано!\n")

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

        # Встановлення локалі для української мови
        locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')

        for contact in self.contacts:
            name = contact.name.value
            birthday = contact.birthday
            if birthday is None or not birthday.is_valid():
                continue

            birthday_date = datetime.strptime(birthday.value, '%d.%m.%Y').date()
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

        # Повернення локалі на мову за замовчуванням
        locale.setlocale(locale.LC_TIME, '')

        return matching_birthdays