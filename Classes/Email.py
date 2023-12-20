from .Field import Field
import re

class Email(Field):
    def __init__(self, value=''):
        super().__init__(value)

    def is_valid(self):
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_pattern, str(self.value)) is not None