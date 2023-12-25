import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
from rich import print
from models.methods import *
from models.contact_operations import delete_contact
from prompt_toolkit import prompt, completion


def change_contact_menu():
    print(
        "////////////////////////////////////////////////////////////////////////////////////////////////////////"
    )
    print("   Опції оновлення контакту:")
    print("     1. Додати/редагувати номер телефону")
    print("     2. Редагувати E-mail")
    # print("     3. Редагувати день народження")
    print("     4. Редагувати нотатки")
    print("     5. Видалити нотатки")
    print("     0. Повернутися до головного меню")


def change_contact(name):
    # name = name[0]

    change_contact_menu()
    print(
        "////////////////////////////////////////////////////////////////////////////////////////////////////////"
    )
    choice = input("Оберить що саме хочете змінити: ")

    if choice == "1":
        try:
            print(edit_phone(name.name.value))
        except KeyError as e:
            print(e)
    elif choice == "2":
        try:
            edit_email(name.name.value)
        except KeyError as e:
            print(e)
    # elif choice == "3":
    #    try:
    #        current_contact = validate_contact()
    #        edit_birthday(name.name.value)
    #    except KeyError as e:
    #        print(e)
    elif choice == "4":
        if len(name.notes) == 0:
            print(
                f"[red]Жодної нотатки до контакту [yellow bold]{name.name.value}[/yellow bold] ще не було додано[/red]"
            )
            return
        else:
            try:
                print(edit_note(name))
            except KeyError as e:
                print(e)

    elif choice == "5":
        if len(name.notes) == 0:
            print(
                f"[red]Жодної нотатки до контакту [yellow bold]{name.name.value}[/yellow bold] ще не було додано[/red]"
            )
            return
        else:
            print(delete_note(name))

    else:
        print(
            "[red]Invalid choice. Please enter a [/red][yellow bold]valid option number.[/yellow bold]"
        )

    return ""


def main_menu():
    print(
        "////////////////////////////////////////////////////////////////////////////////////////////////////////"
    )
    print("Привіт!:")
    print("1. Додати контакт")
    print("2. Обновити контакт")
    print("3. Додати нотатки")
    print("4. Пошук контакта")
    print("5. Показати книгу контаків")
    print("6. Дні народження")
    print("9. Видалити контакт")
    print("0. Хочешь вийти? Тицяй 0")


def main():
    print(
        "////////////////////////////////////////////////////////////////////////////////////////////////////////"
    )
    print("Зроблю що захочешь")

    console = Console()

    while True:
        main_menu()

        print("")
        user_input = input("Введи номер команди: ")

        if user_input == "1":
            print(
                "////////////////////////////////////////////////////////////////////////////////////////////////////////"
            )
            print("[yellow]Ти вибрав: Добавити контакт[/yellow]")
            result = add_contact(None)
            if isinstance(result, Exception):
                print(
                    f"[red]An error occurred: [/red][yellow bold]{result}[/yellow bold]"
                )
            else:
                print(result)

        elif user_input == "2":
            if all_contacts():
                print(
                    "////////////////////////////////////////////////////////////////////////////////////////////////////////"
                )
                print("[yellow]Ти вибрав: Обновити контакт[yellow]")
                try:
                    change_contact(validate_contact())
                except KeyError as e:
                    print(e)
            else:
                print("[red]Жодного контакту ще не було додано[/red]")

        elif user_input == "3":
            print(
                "////////////////////////////////////////////////////////////////////////////////////////////////////////"
            )
            if all_contacts():
                print(add_notes())
            else:
                print("[red]Жодного контакту ще не було додано[/red]")
        elif user_input == "4":
            print(
                "////////////////////////////////////////////////////////////////////////////////////////////////////////"
            )
            search_name = input(
                "Введіть ім'я для пошуку, номер телефону, електронну адресу або нотатки: "
            )
            found_contact = find_contact(search_name)
            if found_contact:
                print(
                    f"[green]Знайдено контакт:[/green] [yellow bold]{found_contact}[/yellow bold]"
                )
            else:
                print("[red]Контакт не знайдено[/red]")

            # Тут виклик функціі, яка знаходить контакт
        elif user_input == "5":
            # Тут виклик функціі, яка виводить всі контакти
            print(
                "////////////////////////////////////////////////////////////////////////////////////////////////////////"
            )
            show_all()
        elif user_input == "6":
            print(
                "////////////////////////////////////////////////////////////////////////////////////////////////////////"
            )
            print("")

            try:
                days = int(
                    input("Введіть кількість днів для перевірки днів народження: ")
                )
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
        elif user_input == "9":
            print(
                "////////////////////////////////////////////////////////////////////////////////////////////////////////"
            )
            print("")
            contact_name = input("Введіть ім'я контакту для видалення: ")
            try:
                result = delete_contact(new_book, contact_name)
                print(result)
            except ContactNotFound as e:
                print(f"[red]An error occurred: [/red][yellow bold]{e}[/yellow bold]")

        elif user_input == "0":
            new_book.save_to_disk()
            print("[green]Address book saved to disk.[/green]")
            print("[yellow]Ну па-па![/yellow]")

            break
        else:
            print("[red]]nvalid command number. Please enter a valid option.[/red]")


if __name__ == "__main__":
    main()


tags = []
tags.sort()
