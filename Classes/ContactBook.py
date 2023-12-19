from datetime import datetime
from .Contact import Contact

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
            print(f"Name: {contact.name}\nPhone: {contact.phone_number}\n{'='*30}")

    def upcoming_birthdays(self, days):
        """
        Виводить список контактів, у яких день народження відбудеться через задану кількість днів від поточної дати.
        """
        today = datetime.now().date()
        upcoming_date = today + timedelta(days=days)

        upcoming_birthdays_list = [
            contact for contact in self.contacts
            if contact.birthday and self.validate_birthday(contact.birthday)
            and datetime.strptime(contact.birthday, '%d.%m.%Y').date() == upcoming_date
        ]

        if upcoming_birthdays_list:
            print(f"Контакти з днями народження через {days} днів:")
            for contact in upcoming_birthdays_list:
                print(f"Name: {contact.name}\nBirthday: {contact.birthday}\n{'='*30}")
        else:
            print(f"На жаль, немає контактів з днями народження через {days} днів.")

    def search_contact(self, keyword):
        """Пошук контакту за ключовим словом."""
        results = [contact for contact in self.contacts if keyword.lower() in contact.name.lower()]
        return results