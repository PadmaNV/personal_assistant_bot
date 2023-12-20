from .Field import Field
from datetime import datetime

class Birthday(Field):
    def __init__(self, value=''):
        super().__init__(value)
        self.validation_message = "Дата повинна бути в форматі ДД.ММ.РРРР"

    def is_valid(self):
        try:
            datetime.strptime(str(self.value), '%d.%m.%Y')
            return True
        except ValueError:
            return False