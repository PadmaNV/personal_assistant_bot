class PhoneContainsAlphaSymbols(KeyError):
    pass


class BirthdayFormat(KeyError):
    pass


class PhoneContainsTenSymbols(KeyError):
    pass


class WrongDataFormat(ValueError, KeyError):
    pass


class NewPhoneWasNotProvided(ValueError, KeyError):
    pass


class PhoneWasNotFound(KeyError):
    pass


class WrongPhoneFormat(KeyError):
    pass

class ContactNotFound(Exception):
    def __init__(self, message="Contact not found."):
        self.message = message
        super().__init__(self.message)

class PhoneWasNotFound(Exception):
    def __init__(self, message="Phone not found."):
        self.message = message
        super().__init__(self.message)

class BirthdayNotFound(Exception):
    def __init__(self, message="Birthday not found."):
        self.message = message
        super().__init__(self.message)

class EmailNotFound(Exception):
    def __init__(self, message="Email not found."):
        self.message = message
        super().__init__(self.message)

class NoteNotFound(Exception):
    def __init__(self, message="Note not found."):
        self.message = message
        super().__init__(self.message)


class WrongEmailFormat(KeyError):
    pass

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except WrongPhoneFormat:
            print("\033[91mGive me phone please\033[0m")
        except WrongEmailFormat:
            print("\033[91msome shit\033[0m")
        except BirthdayFormat:
            print("\033[91mPlease be sure that provided format is applicable,\nformat for birthday adding: 'name' 'birthday'\033[0m")
        except PhoneWasNotFound:
            print("\033[91mWe cannot find this phone number, please try it again\033[0m")
        except NewPhoneWasNotProvided:
            print("\033[91mPlease be sure that provided format is applicable,\nformat for phone changing: 'name' 'old phone number' 'new phone number'\033[0m")
        except WrongDataFormat:
            print("\033[91mPlease be sure that provided format is applicable,\nallowed data format: DD.MM.YYYY\033[0m")
        except PhoneContainsTenSymbols:
            print("\033[91mPhone must contain strictly 10 numbers, please try it again.\033[0m")
        except PhoneContainsAlphaSymbols:
            print("\033[91mPhone cannot contain letters, please try it again.\033[0m")
        except ValueError:
            print("\033[91mGive me name and phone please.\033[0m")
        except KeyError:
            print("\033[91mSorry, we couldn't find the contact. Please check the name and try again.\033[0m")
        except IndexError:
            print("\033[91mContact name cannot be empty, please try again.\033[0m")

    return inner
