from models.methods import *
from prompt_toolkit import prompt,completion


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





#to do Denys
def parse_input(user_input):   
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args
   

def change_contact_menu():
    print("Редагування контакту:")
    print("1. Додати/редагувати номер телефону")
    print("2. Редагувати E-mail")
    print("4. Редагувати нотатки")
    print("0. Повернутися до головного меню")

def main():
    print("Зроблю що захочешь")
    while True:
        user_input = input("Введи номер команди (або 'help' для виведення меню): ").strip()

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
                name_to_edit = prompt("Оберить ім'я контакту із списку вишче: ", completer=completion.WordCompleter(contacts))
                change_contact([name_to_edit])
                change_contact_menu()
                choice = input("Оберіть номер опції, яку хочете виконати: ").strip()

                if choice == "1":
                    new_book.add_phone_menu(name_to_edit)
                elif choice == "2":
                    if all_contacts():
                        print("Ви вибрали: Редагувати E-mail")
                        print(all_contacts())
                        contacts = collect_contacts()
                        name_to_edit = prompt("Оберіть ім'я контакту із списку вище: ", completer=completion.WordCompleter(contacts))
                        new_book.edit_email(name_to_edit)
                    else:
                        print("Жодного контакту ще не було додано")
                elif choice == "3":
                    new_book.edit_birthday(name_to_edit)
                elif choice == "0":
                    print("Повернення до головного меню.")
                    main()

                else:
                    print("Невірний номер опції. Будь ласка, введіть правильну опцію.")
            else:
                print("Жодного контакту ще не було додано")


        elif user_input == "3": 
            if all_contacts():
                print(all_contacts())
                contacts = collect_contacts()                
                contact_name = prompt("Оберить ім'я контакту із списку вишче: ", completer=completion.WordCompleter(contacts))
                found_contact =  find_contact(contact_name)
                new_notes = input("Вкажить які саме нотатки бажаєте додати: ")
                add_notes(found_contact,new_notes)
            else:
                print("Жодного контакту ще не було додано")            
        elif user_input == "4":
            search_name = input("Введіть ім'я для пошуку, номер телефону або електронну адресу: ")
            found_contact = find_contact(search_name)
            if found_contact:
                print(f"Знайдено контакт: {found_contact}")
            else:
                print("Контакт не знайдено")
        elif user_input == "5":            
            # Тут виклик функціі, яка виводить всі контакти
            print(all_contacts())
        elif user_input == "6":
            print("")
            try:
                days = int(input("Введіть кількість днів для перевірки днів народження: "))
            except ValueError:
                print("Невірний ввід. Будь ласка, введіть правильне число.")
                continue

            upcoming_birthdays = new_book.get_birthdays(days)
            
            if upcoming_birthdays:
                print(f"Дні народження протягом наступних {days} днів:")
                for birthday_info in upcoming_birthdays:
                    print(birthday_info)
            else:
                print(f"Немає днів народження протягом наступних {days} днів.")
        elif user_input == "7":
            print("")
            # Тут виклик функціі, яка видаляє контакт
        elif user_input == "0":
            new_book.save_to_disk()
            print("Address book saved to disk.")
            print("Ну па-па!")
            
            break

        elif user_input.lower() == "help":
            print("Меню команд:")
            print("1. Додати контакт")
            print("2. Обновити контакт")
            print("3. Редагувати день народження")
            print("4. Додати нотатки")
            print("5. Знайти контакт")
            print("6. Показати всі контакти")
            print("7. Найближчі дні народження")
            print("8. Видалити контакт")
            print("0. Вихід/зберегти у файл")
        else:
            print("Невідома команда. Введіть 'help' для виведення меню команд.")


if __name__ == "__main__":
    main()