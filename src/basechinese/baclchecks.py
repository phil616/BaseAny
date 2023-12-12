import math
from basechinese.exceptions import (
    DuplicationException,
    UnPrintableException,
    NotEnoughLengthException,
)


def check_duplicates(s: str) -> None:
    """
    check if there are any duplicates in the string
    [one of the precheck functions in BACL's checking sequence]
    Args:
        s (str): the string to check
    Raises:
        DuplicationException: if there are duplicates
    Returns:
        None
    """
    char_indices = {}
    duplicates = {}

    for index, char in enumerate(s):
        if char in char_indices:
            # if char has shown before, add it to duplicates dict
            if char in duplicates:
                duplicates[char].append(index)
            else:
                duplicates[char] = [char_indices[char], index]
        else:
            char_indices[char] = index
    if duplicates:
        raise DuplicationException(duplicates)


def check_isprintable(s: str) -> None:
    """
    check if the string contains unprintable characters
    [one of the precheck functions in BACL's checking sequence]
    Args:
        s (str): the string to check
    Raises:
        UnPrintableException: if there are unprintable characters
    Returns:
        None
    """
    non_printable = []
    for index, char in enumerate(s):
        if not char.isprintable():
            non_printable.append((index, repr(char)))
    if non_printable:
        raise UnPrintableException(
            non_printable, "The string contains unprintable characters"
        )


def check_BACL_available(s: str) -> None:
    """
    check if the string is BACL available
    [one of the precheck functions in BACL's checking sequence]
    Args:
        s (str): the string to check
    Raises:
        NotEnoughLengthException: if the string is not BACL available
    Returns:
        None
    """
    STRING_LENGTH = len(s)
    log_ret = math.log2(STRING_LENGTH)
    available_digits = math.floor(log_ret)
    AD = available_digits
    padding_chars = AD - 1
    PC = padding_chars
    if PC + 2**AD > STRING_LENGTH:
        raise NotEnoughLengthException(
            AD=AD, PC=PC, BL=STRING_LENGTH, message="The string is not BACL available"
        )
