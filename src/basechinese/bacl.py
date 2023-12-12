"""
Basic Available Character List
"""
import math
from basechinese.baclchecks import (
    check_duplicates,
    check_isprintable,
    check_BACL_available,
)


class BACL(dict):
    """
    Basic Available Character List

    Args:
        ms (str, optional): the string to initialize. Defaults to None.
    Attributes:
        ORIGINAL_STRING (str): the original string
    Methods:
        get_available_digits: get the available digits for encoding
        get_padding_chars_number: get the number of padding chars
        get_padding_chars: get the padding chars
        get_max_border: get the max border of the mapping
        get_reverse_dict: get the reverse dict
    Usage:
        >>> from basechinese.bacl import BACL
        >>> bacl = BACL("0123456789")
        >>> bacl.get_available_digits()
        4
        >>> bacl.get_padding_chars_number()
        3
        >>> bacl.get_padding_chars()
        {16: '0', 17: '1', 18: '2'}
        >>> bacl.get_max_border()
        16
        >>> bacl.get_reverse_dict()
        {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
        '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}

    """
    def __init__(self, ms: str = None):
        """init the BACL"""
        self.ORIGINAL_STRING = ms
        self._precheck()
        # Construct the dict
        for index, char in enumerate(self.ORIGINAL_STRING):
            self[index] = char

    def _precheck(self):
        """precheck the string"""
        checking_sequence: list[callable] = [
            check_isprintable,
            check_duplicates,
            check_BACL_available,
        ]
        for checker in checking_sequence:
            checker(self.ORIGINAL_STRING)

    def get_available_digits(self)->int:
        """get the available digits for encoding"""
        STRING_LENGTH = len(self.ORIGINAL_STRING)
        log_ret = math.log2(STRING_LENGTH)
        return math.floor(log_ret)

    def get_padding_chars_number(self)->int:
        """get the number of padding chars"""
        return self.get_available_digits() - 1

    def get_padding_chars(self) -> dict:
        """get the padding chars"""
        MAPPING_BORDER = 2 ** self.get_available_digits()
        padding_chars = {}
        for i in range(
            MAPPING_BORDER + 1, MAPPING_BORDER + 1 + self.get_padding_chars_number()
        ):
            padding_chars.update({i: self[i]})
        return padding_chars

    def get_max_border(self)->int:
        """get the max border of the mapping"""
        return 2 ** self.get_available_digits()

    def get_reverse_dict(self) -> dict:
        """get the reverse dict"""
        return {v: k for k, v in self.items()}

