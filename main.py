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
    print("4. Редагувати нотатки")
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
                name_to_edit = prompt("Оберить ім'я контакту із списку вишче: ", completer=completion.WordCompleter(contacts))
                change_contact([name_to_edit])
                change_contact_menu()
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
        elif user_input == "0":
            print("Ну па-па!")
            break
        else:
            print("Invalid command number. Please enter a valid option.")


if __name__ == "__main__":
    main()