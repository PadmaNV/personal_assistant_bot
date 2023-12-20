from .Field import Field

class Phone(Field):
    def __init__(self, value=''):
        super().__init__(value)
        self.validation_message = f"{self.__class__.__name__} повинно бути 10 цифр"

    def is_valid(self):
        return self.value.isdigit() and len(self.value) == 10
