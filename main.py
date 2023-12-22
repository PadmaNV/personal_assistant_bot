from models.custom_errors import *
from models import *
from models.functions import Email
from models.functions import Birthday
from models.functions import Phone
from models.functions import Notes
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter





# 1.	Add Contact 
# 2.	Edit/Update 
#   	update/add email
# 	    update/add phone 
#       update birthday
# 3.	Add Notes 
# 4.	Find Contact +/- 
# 5.	All Contact
# 6.	Nearest birthdays
# 7.	Delete Contact 
# 8.	Exit/save to the file


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

    if new_book.find(name):
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

#to do:
#add help
#add print all comands
#rework commands to numbers
#to do Denys


def print_options():
    print("Привіт!:")
    print("1. Добавити контакт")
    print("2. Обновити контакт")
    print("3. Добавити Notes")
    print("4. Пошук контакта")
    print("5. Показати всі збережені контакти")
    print("6. Дні народження")
    print("7. Удалити контакт")
    print("0. Хочешь вийти? Тицяй 0")

def change_contact_menu():
    print("Change contact options:")
    print("1. Додати/редагувати номер телефону")
    print("2. Редагувати E-mail")
    print("3. Редагувати день народження")
    print("0. Повернутися до головного меню")

def main():
    print("Зроблю що захочешь")
    while True:
        print_options()
        user_input = input("Введи номер команди: ")

        if user_input == "1":
            print("Ти вибрав: Добавити контакт")
            result = add_contact(None)
            if isinstance(result, Exception):
                print(f"An error occurred: {result}")
            else:
                print(result)

        elif user_input == "2":
            if all_contacts():
                print("Ти вибрав: Обновити контакт")
                print(all_contacts())
                contacts = collect_contacts()
                name_to_edit = prompt("Оберить ім'я контакту із списку вишче: ", completer=WordCompleter(contacts))
                change_contact([name_to_edit])
                change_contact_menu()
            else:
                print("Жодного контакту ще не було додано")  

        elif user_input == "3": 
            if all_contacts():
                print(all_contacts())
                contacts = collect_contacts()                
                contact_name = prompt("Оберить ім'я контакту із списку вишче: ", completer=WordCompleter(contacts))
                found_contact =  find_contact(contact_name)
                new_notes = input("Вкажить які саме нотатки бажаєте додати: ")
                add_notes(found_contact,new_notes)
            else:
                print("Жодного контакту ще не було додано")            
        elif user_input == "4":
            print("")
            # Тут виклик функціі, яка знаходить контакт
        elif user_input == "5":            
            # Тут виклик функціі, яка виводить всі контакти
            print(all_contacts())
        elif user_input == "6":
            print("")
            # Тут виклик функціі, яка показує дні народження
        elif user_input == "7":
            print("")
            # Тут виклик функціі, яка видаляє контакт
        elif user_input == "8":
            print("Ну па-па!")
            break
        else:
            print("Invalid command number. Please enter a valid option.")


if __name__ == "__main__":
    main()