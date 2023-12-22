from .custom_errors import WrongDataFormat, PhoneWasNotFound, WrongEmailFormat, WrongPhoneFormat
from collections import UserDict, UserList, defaultdict
from datetime import datetime, timedelta, date
import calendar
import re
import locale

class Note(UserDict):
    def __init__(self):
        super().__init__()
        self.tags = [] 

    def __str__(self):
        return ', '.join(f'{key}: {value}' for key, value in self.data.items())    

#Aleksey to do start
class Notes(UserList):
    def __init__(self):
        super().__init__()        


    def add_note(self, notes):
        divider = r',|;|or|\|'
        notes_to_add = re.split(divider, notes)
        for note_text in notes_to_add:
            actual_key = len(self.data) + 1
            new_note = Note()
            new_note[actual_key]=note_text.strip()
            self.data.append(new_note)
            
        
    def find_note(self, note_text):
        result = []      
        for note in self.data:
            for key, value in note.items():            
                if note_text in value:
                    result.append(note)
        return result           
                

    def edit_note(self,note,new_text):
        self.find_note()
        self.data[note-1][note] = new_text  


    def delete_note(self,note=None,all = False):
        if all == False:               
            del self.data[note-1]
        else:            
            while len(self.data)!=0:
                self.data.pop(0)
        return f"The {'note' if all == False else 'Notes'} successfully deleted"        
        
    def add_tag(self,note,tags):
        self.data[note-1].extend(tags)

    def __str__(self):
        return '\n'.join(str(note) for note in self.data)
#Aleksey to end

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Birthday:
    def __init__(self, birthday):
        self.value = self.parse_birthday(birthday)

    def parse_birthday(self, birthday):
        date_format = "%d.%m.%Y"
        while True:
            try:
                if isinstance(birthday, date):
                    return birthday
                else:
                    return datetime.strptime(birthday, date_format).date()
            except ValueError:
                print("Invalid date format. Please enter the date in the format DD.MM.YYYY.")
                birthday = input("Enter birthday (DD.MM.YYYY): ")


class Phone:
    def __init__(self, phone):
        if phone.isnumeric() and len(phone) == 10:
            self.value = phone
        else:
            raise WrongPhoneFormat('Invalid phone format.')
            
            #print("Invalid phone number. Please enter a 10-digit numeric phone number.")


class Email:      
    def __init__(self, email):
        pattern = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+' 
        if re.match(pattern, email):
            self.value = email
        else:
            raise WrongEmailFormat('Invalid email format. Email must be in the format xxx@xxx.xxx') 

        


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = birthday
        self.email = []

    def check_phone_exist(self, phone):
        phone_record = [record for record in self.phones if record.value == phone]
        if len(phone_record) > 0:
            return phone_record
        else:
            raise PhoneWasNotFound

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        return True
        


    def add_email(self, email):
        self.email.append(Email(email))
        return True

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return True

    def find_phone(self, phone):
        for phone in self.check_phone_exist(phone):
            return phone

    def show_birthday(self):
        if self.birthday:
            return self.birthday.value
        return "not provided"

    def edit_phone(self, phone_to_replace, new_phone):
        to_edit = self.remove_phone(phone_to_replace)
        for i in range(to_edit):
            self.add_phone(new_phone)

    def remove_phone(self, phone):
        to_remove = self.check_phone_exist(phone)
        for phone_obj in to_remove:
            self.phones.remove(phone_obj)
        return len(to_remove)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict, Record):
    def add_record(self, record=Record):
        self.data[record.name.value] = record

    #to do Polina
    #add all parametrs to find
    def find(self, name):
        #don't touch start
        
        #don't touch start
        try:
            return self.data[name]
        except:
            return False
        #don't touch end

    #Denys to do start
    
    def get_birthdays(self, days_until_birthday):
        matching_birthdays = []
        today = datetime.today().date()

        # Set locale for Ukrainian language
        locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')

        for key, value in self.data.items():
            name = key
            birthday = value.birthday
            if birthday is None or not birthday.is_valid():
                continue

            birthday_date = datetime.strptime(birthday.value, '%d.%m.%Y').date()
            birthday_this_year = birthday_date.replace(year=today.year)

            if birthday_this_year < today:
                next_year = birthday_this_year.year + 1
                birthday_this_year = birthday_this_year.replace(year=next_year)

            delta_days = (birthday_this_year - today).days

            if 0 <= delta_days <= days_until_birthday:
                day_of_week = birthday_this_year.strftime("%A")
                formatted_date = birthday_this_year.strftime("%d %b %Y").capitalize()
                user_info = f"{name}: {day_of_week}, {formatted_date}"
                matching_birthdays.append(user_info)

        # Reset locale to default language
        locale.setlocale(locale.LC_TIME, '')

        return matching_birthdays


# ... (other classes and functions)

# Update the get_birthdays_per_week method in the main block to call the new get_birthdays method

    #Denys to do end
            
    #to do Vitalii           
    def delete(self, name):
        self.data.pop(name)

#to do Vitalii exit/save   