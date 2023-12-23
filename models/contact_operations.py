from .custom_errors import *

def delete_contact(address_book, name):
    if name in address_book.data:
        contact = address_book.data.pop(name)

        # пов'язані значення (phones, birthday, email)
        for phone in contact.phones:
            phone_value = phone.value
            for record in address_book.data.values():
                try:
                    record.remove_phone(phone_value)
                except PhoneWasNotFound:
                    print(f"Phone {phone_value} not found for contact {name}.")

        if contact.birthday:
            birthday_value = contact.birthday.value
            for record in address_book.data.values():
                try:
                    record.remove_birthday(birthday_value)
                except BirthdayNotFound:
                    print(f"Birthday {birthday_value} not found for contact {name}.")

        for email in contact.emails:
            email_value = email.value
            for record in address_book.data.values():
                try:
                    record.remove_email(email_value)
                except EmailNotFound:
                    print(f"Email {email_value} not found for contact {name}.")

        # метод delete_note у класі Notes
        if hasattr(contact, 'notes'):
            for note in contact.notes:
                try:
                    address_book.delete_note(note)
                except NoteNotFound:
                    print(f"Note {note} not found for contact {name}.")

        return f"Контакт {name} та всі його дані успішно видалені."
    else:
        raise ContactNotFound(f"Contact {name} not found.")