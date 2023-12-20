from .Field import Field

class Name(Field):
    def __init__(self, value=''):
        super().__init__(value)
        self.validation_message = f"{self.__class__.__name__} повинно бути більше 2 букв"

    def is_valid(self):
        return len(self.value) >= 2 and self.value.isalpha()