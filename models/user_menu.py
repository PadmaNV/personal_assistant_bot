from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from .functions import AddressBook

# Define a list of fruits
def collect_contacts():
    contacts = []
    for contact in AddressBook.keys():
        contacts.append(contact)
    return contacts


# Create a completer for the fruit names
fruit_completer = WordCompleter(fruits)

# Prompt the user to choose a fruit
selected_fruit = prompt('Choose a fruit: ', completer=fruit_completer)
print(f'You selected: {selected_fruit}')

# Menu for actions on the selected fruit
action_completer = WordCompleter(['edit', 'delete'])

# Prompt the user to choose an action for the selected fruit
selected_action = prompt('Choose an action (edit/delete): ', completer=action_completer)
print(f'You selected action: {selected_action}')
