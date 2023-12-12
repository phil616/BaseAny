"""
Basic Available Character List
This project is under development
"""
import math
from basechinese.baclchecks import (
    check_duplicates,
    check_isprintable,
    check_BACL_available,
)


class BACL(dict):
    def __init__(self, ms: str = None):
        self.ORIGINAL_STRING = ms
        self._precheck()
        # construct the dict

        for index, char in enumerate(self.ORIGINAL_STRING):
            self[index] = char

    def _precheck(self):
        checking_sequence: list[callable] = [
            check_isprintable,
            check_duplicates,
            check_BACL_available,
        ]
        for checker in checking_sequence:
            checker(self.ORIGINAL_STRING)

    def get_available_digits(self):
        STRING_LENGTH = len(self.ORIGINAL_STRING)
        log_ret = math.log2(STRING_LENGTH)
        return math.floor(log_ret)

    def get_padding_chars_number(self):
        return self.get_available_digits() - 1

    def get_padding_chars(self) -> dict:
        MAPPING_BORDER = 2 ** self.get_available_digits()
        padding_chars = {}
        for i in range(
            MAPPING_BORDER + 1, MAPPING_BORDER + 1 + self.get_padding_chars_number()
        ):
            padding_chars.update({i: self[i]})
        return padding_chars

    def get_max_border(self):
        return 2 ** self.get_available_digits()

    def get_reverse_dict(self) -> dict:
        return {v: k for k, v in self.items()}

