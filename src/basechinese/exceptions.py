"""
This module contains the set of BaseChinese' exceptions.s
"""

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
    def __init__(self, AD:int,PC:int,BL:int,message="Not Enough Length for BACL"):
        self.message = message
        self.AD = AD
        self.PC = PC
        self.BL = BL
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: Make sure PC + 2^AD > BACL_LENGTH, but now PC={self.PC},AD={self.AD},BACL_LENGTH={self.BL} "

class InputTypeException(BaseException):
    def __init__(self,inputType:type,message="Input Type Error"):
        self.message = message
        self.inputType = inputType
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.inputType} is not allowed "
