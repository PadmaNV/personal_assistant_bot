from Classes.ContactBook import ContactBook

def display_menu():
    print("1. Додати контакт")
    print("2. Пошук контакту")
    print("3. Показати всі контакти")
    print("4. Вивести контакти з днями народження через задану кількість днів")
    print("0. Вийти")

def main():
    my_contact_book = ContactBook()

    while True:
        display_menu()
        choice = input("Виберіть опцію: ")

        if choice == "1":
            my_contact_book.add_contact_interactive()

        elif choice == "2":
            search_keyword = input("Введіть ключове слово для пошуку: ")
            search_results = my_contact_book.search_contact(search_keyword)
            print(f"Результати пошуку для '{search_keyword}':")
            for result in search_results:
                print(f"Name: {result.name}\nPhone: {result.phone_number}\n{'='*30}")
            print()

        elif choice == "3":
            print("Всі контакти:")
            my_contact_book.display_contacts()
            print()

        elif choice == "4":
            days = int(input("Введіть кількість днів для перевірки днів народження: "))
            matching_birthdays = my_contact_book.get_birthdays(days)

            if matching_birthdays:
                print("Контакти з днями народження протягом наступних днів:")
                for birthday_info in matching_birthdays:
                    print(birthday_info)
            else:
                print(f"Немає контактів з днями народження протягом наступних {days} днів.")
            print()

        elif choice == "0":
            print("Дякую за використання бота. До побачення!")
            break

        else:
            print("Невірний вибір. Спробуйте ще раз.\n")

if __name__ == "__main__":
    main()