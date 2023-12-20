class Contact:
    def __init__(self, name, address, phone_number, email, birthday):
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.birthday = birthday

from .Field import Field
from .Name import Name

class Contact:
    def __init__(self, name, address, phone_number, email, birthday):
        self.name = Name(name)
        self.address = Field(address)
        self.phone_number = Field(phone_number)
        self.email = Field(email)
        self.birthday = Field(birthday)
