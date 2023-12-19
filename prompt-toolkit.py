from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

# список користувачів (приклад)
users = [
    'user1',
    'user2',
    'user3',
    # додати більше користувачів
]

# встановлюємо підказку для випадаючого списку
completer = WordCompleter(users, ignore_case=True)

if __name__ == '__main__':
    # використовуємо prompt_toolkit для отримання введення від користувача
    selected_user = prompt('Виберіть користувача: ', completer=completer)

    # виведення вибору користувача
    print('Вибраний користувач: %s' % selected_user)