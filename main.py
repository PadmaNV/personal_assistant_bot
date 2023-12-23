from models.methods import *
from models.contact_operations import delete_contact
from prompt_toolkit import prompt, completion

def change_contact_menu():
    print("Change contact options:")
    print("1. Додати/редагувати номер телефону")
    print("2. Редагувати E-mail")
    print("3. Редагувати день народження")
    print("4. Редагувати нотатки")
    print("5. Видалити нотатки")
    print("0. Повернутися до головного меню")

def change_contact(name):
    #name = name[0]    


    change_contact_menu()
    choice = input("Оберить що саме хочете змінити: ")

    if choice == "1":
        edit_phone(name)
    elif choice == "2":
        edit_email(name)
    elif choice == "3":
        edit_birthday(name)
    elif choice == "4":
        if len(name.notes) == 0:
            print( f"Жодної нотатки до контакту {name.name.value} ще не було додано")
            return
        else:
            try:
                edit_note(name)                
                print(edit_note(name))
            except KeyError as e:
                    print(e)  
                    
    elif choice == "5":
        if len(name.notes) == 0:
            print( f"Жодної нотатки до контакту {name.name.value} ще не було додано")
            return
        else:
            print(delete_note(name))      

    else:
        print("Invalid choice. Please enter a valid option number.")

    return ""

def main_menu():
    print("Привіт!:")
    print("1. Додати контакт")
    print("2. Обновити контакт")
    print("3. Додати нотатки")
    print("4. Пошук контакта")
    print("5. Показати всі збережені контакти")
    print("6. Дні народження")
    print("7. Видалити контакт")
    print("0. Хочешь вийти? Тицяй 0")

def main():
    print("Зроблю що захочешь")
    while True:
        main_menu()

def parse_input(user_input):   
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


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
                try:                
                    change_contact(validate_contact())
                except KeyError as e:
                    print(e)                 
            else:
                print("Жодного контакту ще не було додано")  

        elif user_input == "3": 
            if all_contacts():
                print(add_notes())
            else:
                print("Жодного контакту ще не було додано")            
        elif user_input == "4":
            contact_name = input("Введіть ім'я контакту для видалення: ")
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
            contact_name = input("Введіть ім'я контакту для видалення: ")
            try:
                result = delete_contact(new_book, contact_name)
                print(result)
            except ContactNotFound as e:
                print(f"An error occurred: {e}")
                
            # Тут виклик функціі, яка видаляє контакт
        elif user_input == "0":
            new_book.save_to_disk()
            print("Address book saved to disk.")
            print("Ну па-па!")
            
            break
        else:
            print("Invalid command number. Please enter a valid option.")


if __name__ == "__main__":
    main()