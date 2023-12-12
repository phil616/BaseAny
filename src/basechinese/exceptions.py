class BaseException(Exception):
    pass


class DuplicationException(BaseException):
    def __init__(self, duplicates:dict={},message="BasicAvailableCharacterList Duplication"):
        self.message = message
        self.duplicates = duplicates
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.duplicates} "

class UnPrintableException(BaseException):
    def __init__(self, unprintablechars:list,message="Unprintable Character Detected"):
        self.message = message
        self.unprintablechars = unprintablechars
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.unprintablechars} "

class NotEnoughLengthException(BaseException):
    pass

class InputTypeException(BaseException):
    pass