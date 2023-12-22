from models.custom_errors import *
from models import *

new_book = AddressBook()

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
            print("Invalid phone number. Please enter a 10-digit numeric phone number.")

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
    print("Current phone numbers:")
    for i, phone in enumerate(current_contact.phones, 1):
        print(f"{i}. {phone.value}")

    while True:
        try:
            choice = int(input("Select a phone number to edit (or 0 to go back): "))
            if 0 <= choice <= len(current_contact.phones):
                break
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    if choice == 0:
        return

    new_phone = input("Enter the new phone number: ")
    current_contact.phones[choice - 1] = Phone(new_phone)
    print("Phone number successfully updated.")

def edit_email(name):
    current_contact = find_contact(name)
    print("Current email addresses:")
    for i, email in enumerate(current_contact.email, 1):
        print(f"{i}. {email.value}")

    while True:
        try:
            choice = int(input("Select an email address to edit (or 0 to go back): "))
            if 0 <= choice <= len(current_contact.email):
                break
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    if choice == 0:
        return

    new_email = input("Enter the new email address: ")
    try:
        current_contact.email[choice - 1] = Email(new_email)
        print("Email address successfully updated.")
    except WrongEmailFormat:
        print("Invalid email address. Please enter a valid email.")

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
        print("Invalid choice. Please enter a valid option number.")

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
