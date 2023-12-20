from .Name import Name
from .Field import Field
from .Phone import Phone
from .Email import Email
from .Birthday import Birthday

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.address = None
        self.email = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_address(self, address):
        self.address = Field(address)

    def add_email(self, email):
        self.email = Email(email)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)