from .custom_errors import WrongDataFormat, PhoneWasNotFound, WrongEmailFormat
from collections import UserDict, UserList, defaultdict
from datetime import datetime, timedelta
import calendar
import pickle
import re

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
        date_format = "%d.%m.%Y"
        try:
            self.value = datetime.strptime(birthday, date_format).date()
        except ValueError:
            raise WrongDataFormat


class Phone(Field):
    pass


class Email:      
    def __init__(self, email):
        pattern = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+' 
        if re.match(pattern, email):
            self.value = email
        else:
            raise WrongEmailFormat('Invalid email format') 

        


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
        for phone in to_remove:
            self.phones.remove(phone)
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
    def get_birthdays_per_week(self):
        def next_monday(birthday_this_year, delta_days):
            for i in range(7 - delta_days):
                if (birthday_this_year + timedelta(days=i)).weekday() == 0:
                    return True
                else:
                    i += 1

        def append_users_birthday(birthday_weekday, name):
            users_birthday[birthday_weekday].append(name)

        weekend_days = [5, 6]
        users_birthday = defaultdict(list)
        users_birthday = {0: [], 1: [], 2: [], 3: [], 4: []}
        today_date = datetime.today().date()

        for key, value in self.data.items():
            name = key
            if value.birthday is None:
                continue
            else:
                birthday = value.birthday.value
                birthday_this_year = (
                    birthday.replace(year=today_date.year + 1)
                    if birthday.replace(year=today_date.year) < today_date
                    else birthday.replace(year=today_date.year)
                )
                delta_days = (birthday_this_year - today_date).days
                if delta_days < 7:
                    if birthday_this_year.weekday() in weekend_days and next_monday(
                        birthday_this_year, delta_days
                    ):
                        append_users_birthday(0, name)
                    elif birthday_this_year.weekday() not in weekend_days:
                        append_users_birthday(birthday_this_year.weekday(), name)

        for key, value in users_birthday.items():
            if value:
                return (f"{calendar.day_name[key]:<9}: {', '.join(value):<}")
            else:
                return "No scheduled birthdays for the upcoming week"
    #Denys to do end


    def save_to_disk(self, filename="address_book.pkl"):
        with open(filename, "wb") as file:
            pickle.dump(self.data, file)

    def load_from_disk(self, filename="address_book.pkl"):
        try:
            with open(filename, "rb") as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            # If the file is not found, create an empty dictionary
            self.data = {}
        
    #to do Vitalii           
    def delete(self, name):
        self.data.pop(name)

#to do Vitalii exit/save   