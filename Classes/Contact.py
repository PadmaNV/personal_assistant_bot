from .Field import Field
from .Name import Name

class Contact:
    def __init__(self, name, address, phone_number, email, birthday):
        self.data = {
            'name': name,
            'address': address,
            'phone_number': phone_number,
            'email': email,
            'birthday': birthday,
        }

