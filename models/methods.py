from models import *
from models.custom_errors import *
from prompt_toolkit import prompt,completion
from .classes import *
from main import change_contact_menu

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
        raise KeyError('Need to rework')
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
            notes = input("Нотатки: ")                
            break
        except BirthdayFormat as e:
            print(f"Error: {e}")

    if  new_book.find(name):
        contact = new_book.find(name)
        contact.add_phone(phone)
        contact.add_email(email.value)
        contact.add_birthday(birthday.value)
        if notes != "":
            contact.add_notes(notes)
        return f"The new phone number, email, and birthday for the contact {name} successfully added."
    else:        
        new_contact = Record(name)
        new_contact.add_phone(phone)
        new_contact.add_email(email.value)
        new_contact.add_birthday(birthday.value)
        if notes != "":
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

def validate_contact():    
    print(all_contacts())
    contacts = collect_contacts()
    name_to_edit = prompt("Оберить ім'я контакту із списку вишче: ", completer=completion.WordCompleter(contacts))
    if name_to_edit not in contacts:
        raise KeyError("Ви ввели некоректне ім'я")
    found_contact = find_contact(name_to_edit)
    return found_contact

def validate_note(name):
    note_keys = []
    for note in name.notes:
        for key,value in note.items():
            note_keys.append(key)
    return note_keys
   
def edit_note(name):    
    note_to_change = input("Обери номер нотатки яку треба змінити: ")
    if int(note_to_change) not in validate_note(name):
        raise KeyError("Ви ввели некоректний номер нотатки")
    note_new_text = input("Вкажи новий текст нотатки: ")  
    name.notes.edit_note(note_to_change,note_new_text)
    return f"Нотатки під номером {note_to_change} успішно змінена"

def delete_note(name):
    note_to_delete = input("Обери номер нотатки яку треба видалити, для видалення усіх нотаток введить команду all: ")
    if note_to_delete == 'all':
        name.notes.delete_note(all_notes=True)
        return "Усі нотатки успішно видалені"
    elif int(note_to_delete) not in validate_note(name):      
        raise KeyError("Ви ввели некоректний номер нотатки")
    else:
        name.notes.delete_note(note=note_to_delete)    
        return f"Нотатка №{note_to_delete} успішно видалена"
    
@input_error
def add_notes():    
    found_contact =  validate_contact()
    new_notes = input("Додайте нотатки: ")   
    Record.add_notes(found_contact,new_notes)
    return f"Нотатки були додані до контакту {found_contact}"


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
