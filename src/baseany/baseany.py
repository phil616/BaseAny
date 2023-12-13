import math
from typing import Sequence


__all__ = ["anyencode", "anydecode", "MappingList"]

CODE_PAGE = "一二三四五六七八九十"  # CODEPAGE can be replaced to any charset you like

bytes_types = (bytes, bytearray)  # Types acceptable as binary data


def bin2strseq(bytes_data, split=""):
    if not isinstance(bytes_data, bytes_types):
        raise TypeError(f"The input data should be {bytes_types}")
    return split.join(f"{byte:08b}" for byte in bytes_data)


def strseq2bin(strseq):
    if not isinstance(strseq, str):
        raise TypeError(f"The input data should be str instead of {type(strseq)}")
    return bytes(int(strseq[i : i + 8], 2) for i in range(0, len(strseq), 8))


def splitseq_by_len(seq: Sequence, length: int):
    return [seq[i : i + length] for i in range(0, len(seq), length)]


def check_CPN_available(s: str) -> None:
    STRING_LENGTH = len(s)
    log_ret = math.log2(STRING_LENGTH)
    available_digits = math.floor(log_ret)
    AD = available_digits
    padding_chars = AD - 1
    CPN = padding_chars

    if CPN + 2**AD > STRING_LENGTH:
        raise Exception("The string length is not available")


def check_APN_available(s: str) -> None:
    STRING_LENGTH = len(s)
    log_ret = math.log2(STRING_LENGTH)
    available_digits = math.floor(log_ret)
    AD = available_digits
    APN = 1
    if APN + 2**AD > STRING_LENGTH:
        raise Exception(message="The string length is not available")


def check_duplicates(s: str) -> None:
    """
    check if there are any duplicates in the string
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
        raise Exception(duplicates)


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
        raise Exception(non_printable, "The string contains unprintable characters")


class MappingList(list):
    def __init__(self, mapping_list: str, mode: str = "CPN"):
        self.mode = mode
        if mode == "CPN":
            check_CPN_available(mapping_list)
        elif mode == "APN":
            check_APN_available(mapping_list)
        else:
            raise Exception("Mode should be CPN or APN")
        check_duplicates(mapping_list)
        check_isprintable(mapping_list)
        # Check pass
        self.length = len(mapping_list)
        self.mapping = dict(enumerate(mapping_list))
        self.reverse_mapping = {v: k for k, v in self.mapping.items()}

        self.information_entropy = math.log2(self.length)
        self.available_digits = math.floor(self.information_entropy)

        self._max_border = 2**self.available_digits

        self.APN_char = mapping_list[self._max_border]
        self._min_used_length = self._max_border + self.available_digits - 1
        self.CPN_chars = mapping_list[self._max_border : self._min_used_length]

        self = list(mapping_list)

    def __getitem__(self, key):
        return self.mapping[key]

    def get_index(self, key):
        return self.reverse_mapping[key]

    def get_APN_char(self):
        if self.mode == "CPN":
            raise Exception("CPN has no APN char")
        return self.APN_char

    def get_CPN_chars(self):
        if self.mode == "APN":
            raise Exception("APN has no CPN chars")
        return self.CPN_chars

    def get_info(self):
        return {
            "Utilization": self._min_used_length / self.length,
            "MappingList Length": self.length,
            "Minimum Used Length": self._min_used_length,
            "Information Entropy": self.information_entropy,
        }


def anyencode(bytes_data: bytes, mode="CPN") -> str:
    ML = MappingList(CODE_PAGE, mode=mode)
    if not isinstance(bytes_data, bytes_types):
        raise TypeError(f"The input data should be {bytes_types}")
    # preprocess
    binary_seq = bin2strseq(bytes_data)  # b'\x01' -> 00000001

    binary_seq_list = splitseq_by_len(
        binary_seq, ML.available_digits
    )  # 00000001 -> ['0000','0001']

    int_seq_list = list(
        map(lambda x: int(x, 2), binary_seq_list)
    )  # ['0000','0001'] -> [0,1]

    last_elem = binary_seq_list[-1]  # 1

    if len(last_elem) < ML.available_digits:  # need padding some extra chars
        padding_zeros = ML.available_digits - len(
            last_elem
        )  # calc how many zeros need to append
        if mode == "CPN":
            cpn_padding_char = ML.get_CPN_chars()[
                padding_zeros - 1
            ]  # get a specific padding char due to the CPN mode
            paddingchars = list(cpn_padding_char)
        else:
            apn_padding_char = ML.get_APN_char()
            paddingchars = [apn_padding_char] * padding_zeros

    else:
        paddingchars = []
    result_list = list(map(lambda x: ML.mapping[x], int_seq_list))
    result_list.extend(paddingchars)
    return "".join(result_list)


def anydecode(char_data: str, mode="CPN") -> bytes:
    ML = MappingList(CODE_PAGE, mode=mode)
    if not isinstance(char_data, str):
        raise TypeError(f"The input data should be str instead of {type(char_data)}")
    char_list = list(char_data)
    last_char = char_list[-1]
    if mode == "CPN":
        if last_char in ML.get_CPN_chars():
            padding_zeros = ML.get_CPN_chars().index(last_char) + 1
            char_list.pop()  # delete padding char
        else:
            padding_zeros = 0
    elif mode == "APN":
        if last_char == ML.get_APN_char():
            padding_zeros = char_list.count(last_char)
            del char_list[-padding_zeros:]  # delete padding chars
        else:
            padding_zeros = 0
    else:
        raise Exception("Mode should be CPN or APN")
    int_seq = list(
        map(lambda x: ML.reverse_mapping[x], char_list)
    )  # ['一','二'] -> [0,1]

    binary_seq = "".join(
        map(lambda x: format(x, f"0{ML.available_digits}b"), int_seq)
    )  # [0,1] -> '00000001'
    binary_seq = (
        binary_seq[:-padding_zeros] if padding_zeros > 0 else binary_seq
    )  # delete padding zeros

    bytes_data = strseq2bin(binary_seq)  # '00000001' -> b'\x01'

    return bytes_data
