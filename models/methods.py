from rich import print
from rich.console import Console
from rich.table import Table
from models.custom_errors import *
from models import *
from models.custom_errors import *
from prompt_toolkit import prompt,completion
from .classes import *
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
#add all parametrs to findd
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
            print("[red]Invalid phone number. Please enter a [/red][bold yellow]10-digit numeric phone number.[/bold yellow]")

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
            print(f"[red]Error: [/red][yellow bold]{e}[/yellow bold]")
    
    while True:
        try:
            notes = input("Нотатки: ")                
            break
        except BirthdayFormat as e:
            print(f"[red]Error: [/red][yellow bold]{e}[/yellow bold]")

    if  new_book.find(name):
        contact = new_book.find(name)
        contact.add_phone(phone)
        contact.add_email(email.value)
        contact.add_birthday(birthday.value)
        if notes != "":
            contact.add_notes(notes)
        return f"[green]The new phone number, email, and birthday for the contact [yellow bold]{name}[/yellow bold] successfully added.[/green]"
    else:        
        new_contact = Record(name)
        new_contact.add_phone(phone)
        new_contact.add_email(email.value)
        new_contact.add_birthday(birthday.value)
        if notes != "":
            new_contact.add_notes(notes)        
        new_book.add_record(new_contact)        
        return f"[green]Contact [yellow bold]{name}[/yellow bold] successfully added.[/green]"

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
        new_phone = input("Введіть новий номер телефону: ")
        try:
            current_contact.add_phone(new_phone)
            print("Номер телефону успішно доданий.")
        except WrongPhoneFormat:
            print("Невірний формат номеру телефону. Будь ласка, введіть правильний номер.")
    else:
        new_phone = input("Введіть новий номер телефону: ")
        try:
            current_contact.edit_phone(phone_choice - 1, new_phone)
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

  
def edit_birthday(name):
    current_contact = find_contact(name)
    
    print(f"Current birthday: {current_contact.birthday}")
    
    new_birthday_str = input("Enter the new birthday (DD.MM.YYYY): ")
    
    new_birthday = Birthday.from_string(new_birthday_str)
    
    if current_contact.add_birthday(new_birthday):
        print("Birthday successfully updated.")
    else:
        print("Failed to update birthday. Please enter a valid date format (DD.MM.YYYY).")

def validate_contact():    
    show_all()
    contacts = collect_contacts()
    name_to_edit = prompt("Оберить ім'я контакту із списку вишче: ", completer=completion.WordCompleter(contacts))
    if name_to_edit not in contacts:
        raise KeyError("[red]Ви ввели некоректне ім'я[/red]")
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
        raise KeyError("[red]Ви ввели некоректний номер нотатки[/red]")
    note_to_change_obj = name.notes.find_note_by_key(note_to_change)
    note_new_text = input("Вкажи новий текст нотатки: ")  
    name.notes.edit_note(note_to_change_obj,note_to_change,note_new_text)
    return f"[green]Нотатки під номером [yellow bold]{note_to_change}[/yellow bold] успішно змінена[/green]"

def delete_note(name):
    note_to_delete = input("Обери номер нотатки яку треба видалити, для видалення усіх нотаток введить команду all: ")
    if note_to_delete == 'all':
        name.notes.delete_note(all_notes=True)
        return "[green]Усі нотатки успішно видалені[/green]"
    elif int(note_to_delete) not in validate_note(name):      
        raise KeyError("[red]Ви ввели некоректний номер нотатки[/red]")
    else:
        note_to_delete = name.notes.find_note_by_key(note_to_delete)
        name.notes.delete_note(note_to_delete)    
        return f"[green]Нотатка [yellow bold]№{note_to_delete}[/yellow bold] успішно видалена[/green]"
    
@input_error
def add_notes():    
    found_contact =  validate_contact()
    new_notes = input("Додайте нотатки: ")   
    Record.add_notes(found_contact,new_notes)
    return f"[green]Нотатки були додані до контакту [/green][yellow bold]{found_contact}[/yellow bold]"


@input_error
def add_birthday(args):
    try:
        name, birthday = args
    except:
        raise BirthdayFormat

    if not Record.add_birthday(find_contact(name), birthday):
        raise WrongDataFormat
    return f"[green]Birthday for the contact [yellow bold]{name} [/yellow bold]successfully added.[/green]"

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
            return f"[green]Email for the contact [yellow bold]{name}[/yellow bold] successfully added.[/green]"
        except WrongEmailFormat as e:
            print(f"[red]Error: [/red][yellow bold]{e}[/yellow bold]")
            email = input("Please enter a valid email: ")

@input_error
def show_birthday(args):
    name = args[0]

    birthday = Record.show_birthday(find_contact(name))
    return f"[yellow]Contact [bold]{name}[/bold] birthday: [bold]{birthday}[/bold][/yellow]"


@input_error
def show_phone(args):
    name = args[0]
    return find_contact(name)


@input_error
def show_all():
    console = Console()
    if not new_book.data:
        console.print("[red]Немає доступних контактів[/red]")
        return

    table = Table(title="Книга усіх контактів")
    table.add_column("Ім'я", justify="center", style="cyan", no_wrap=True)
    table.add_column("Номер телефону", justify="center", style="magenta", no_wrap=True)
    table.add_column("Мейл", justify="center", style="yellow", no_wrap=True)
    table.add_column("День народження", justify="center", style="green", no_wrap=True)
    table.add_column("Нотатки", justify="center", style="blue", no_wrap=True)

    for contact_name, contact in new_book.data.items():
        phones = ", ".join([phone.value for phone in getattr(contact, 'phones', [])])
        emails = ", ".join([email.value for email in getattr(contact, 'emails', [])]) if hasattr(contact, 'emails') else ''
        birthday = getattr(contact, 'show_birthday', lambda: '')().strftime('%d.%m.%Y')
        notes = getattr(contact, 'notes', '') 
       
        table.add_row(contact_name, phones, emails, str(birthday), str(notes))

    console.print(table)
