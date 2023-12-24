from models.custom_errors import *
from models import *
from main import change_contact_menu, main

new_book = AddressBook()
new_book.load_from_disk()

def collect_contacts():
    contacts = []
    for key in new_book.keys():
        contacts.append(key)
    return contacts

#to do Denys
def parse_input(user_input):   
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args
   
def all_contacts():
    if len(new_book) ==0:
        return False
    for record in new_book.data.values():
        return record

#to do Polina
#add all parametrs to find
def find_contact(name):
    found_contact = new_book.find(name)
    if found_contact == False:
        raise KeyError
    else:
        return found_contact

#need to validate exist number or not
@input_error
def add_contact(args):
    name = input("Ім'я контакту: ")

    while True:
        phone = input("Номер телефону: ")
        if phone.isnumeric() and len(phone) == 10:
            break
        else:
            print("Невірний номер.Номер повинен бути з 10 цифр")

    while True:
        try:
            email = Email(input("E-mail: "))
            break
        except WrongEmailFormat as e:
            print(f"Error: {e}")

    while True:
        try:
            birthday = Birthday(input("Дата народження (DD.MM.YYYY): "))
            break
        except BirthdayFormat as e:
            print(f"Error: {e}")
    
    while True:
        try:
            notes = input("Вкажить які саме нотатки бажаєте додати: ")                
            break
        except BirthdayFormat as e:
            print(f"Error: {e}")

    if  new_book.find(name):
        contact = new_book.find(name)
        contact.add_phone(phone)
        contact.add_email(email.value)
        contact.add_birthday(birthday.value)
        contact.add_notes(notes)
        return f"The new phone number, email, and birthday for the contact {name} successfully added."
    else:        
        new_contact = Record(name)
        new_contact.add_phone(phone)
        new_contact.add_email(email.value)
        new_contact.add_birthday(birthday.value)
        new_contact.add_notes(notes)
        new_book.add_record(new_contact)        
        return f"Contact {name} successfully added."


def edit_phone(name):
    current_contact = find_contact(name)
    print("Існуючі номери телефонів:")
    for i, phone in enumerate(current_contact.phones, 1):
        print(f"{i}. {phone.value}")

    while True:
        try:
            phone_choice = int(input("Виберіть номер телефону для редагування (або введіть 0 для додавання нового): "))
            if 0 <= phone_choice <= len(current_contact.phones):
                break
            else:
                print("Невірний вибір. Будь ласка, введіть правильний номер.")
        except ValueError:
            print("Невірний ввід. Будь ласка, введіть номер.")

    if phone_choice == 0:
        # Додаємо новий номер телефону
        new_phone = input("Введіть новий номер телефону: ")
        try:
            current_contact.add_phone(new_phone)
            print("Номер телефону успішно доданий.")
        except WrongPhoneFormat:
            print("Невірний формат номеру телефону. Будь ласка, введіть правильний номер.")
    else:
        # Редагуємо існуючий номер телефону
        new_phone = input("Введіть новий номер телефону: ")
        try:
            current_contact.phones[phone_choice - 1] = Phone(new_phone)
            print("Номер телефону успішно оновлено.")
        except WrongPhoneFormat:
            print("Невірний формат номеру телефону. Будь ласка, введіть правильний номер.")

def edit_email(name):
    current_contact = find_contact(name)
    print("Існуючі електронні адреси:")
    for i, email in enumerate(current_contact.emails, 1):
        print(f"{i}. {email.value}")

    while True:
        try:
            email_choice = int(input("Виберіть номер електронної адреси для редагування (або введіть 0 для додавання нової): "))
            if 0 <= email_choice <= len(current_contact.emails):
                break
            else:
                print("Невірний вибір. Будь ласка, введіть правильний номер.")
        except ValueError:
            print("Невірний ввід. Будь ласка, введіть номер.")

    if email_choice == 0:
        # Додаємо новий email
        new_email = input("Введіть новий електронний адрес: ")
        try:
            current_contact.add_email(new_email)
            print("Електронний адреса успішно додана.")
        except WrongEmailFormat:
            print("Невірний формат електронної адреси. Будь ласка, введіть правильний email.")
    else:
        # Редагуємо існуючий email
        new_email = input("Введіть новий електронний адрес: ")
        try:
            current_contact.emails[email_choice - 1] = Email(new_email)
            print("Електронний адреса успішно оновлена.")
        except WrongEmailFormat:
            print("Невірний формат електронної адреси. Будь ласка, введіть правильний email.")

def edit_birthday(name):
    current_contact = find_contact(name)
    current_birthday = current_contact.show_birthday()
    print(f"Current birthday: {current_birthday}")

    while True:
        try:
            new_birthday_str = input("Enter the new birthday (DD.MM.YYYY): ")
            current_contact.add_birthday(Birthday(new_birthday_str).value)
            print("Birthday successfully updated.")
            break
        except WrongDataFormat:
            print("Invalid date format. Please enter the date in the format DD.MM.YYYY.")


@input_error
def change_contact(args):
    name = args[0]
    
    change_contact_menu()
    choice = input("Enter the number of the option you'd like to choose: ")

    if choice == "1":
        edit_phone(name)
    elif choice == "2":
        edit_email(name)
    elif choice == "3":
        edit_birthday(name)
    elif choice == "3":
        edit_birthday(name)
    else:
        print("Повернення до головного меню")
        main()

    return ""
@input_error
def add_notes(contact_name,new_notes):
    Record.add_notes(contact_name,new_notes)



@input_error
def add_birthday(args):
    try:
        name, birthday = args
    except:
        raise BirthdayFormat

    if not Record.add_birthday(find_contact(name), birthday):
        raise WrongDataFormat
    return f"Birthday for the contact {name} successfully added."

@input_error
def add_email(args):
    try:
        name, email = args
    except:
        raise ValueError

    while True:
        try:
            contact = find_contact(name)
            contact.add_email(email)
            return f"Email for the contact {name} successfully added."
        except WrongEmailFormat as e:
            print(f"Error: {e}")
            email = input("Please enter a valid email: ")

@input_error
def show_birthday(args):
    name = args[0]

    birthday = Record.show_birthday(find_contact(name))
    return f"Contact {name} birthday: {birthday}"


@input_error
def show_phone(args):
    name = args[0]
    return find_contact(name)


@input_error
def show_all():
    return new_book.data.items()
