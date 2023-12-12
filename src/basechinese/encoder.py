"""
Convert Bin to BaseChinese
"""

# a mapping from bin to str
from basechinese.codec import load_info
from basechinese.exceptions import InputTypeException


def encode(bytes_data: bytes) -> str:
    if not isinstance(bytes_data, bytes):
        raise InputTypeException("The input data should be bytes")
    codec = load_info()

    binary_strings = ["{:08b}".format(byte) for byte in bytes_data]
    combined_binary_string = "".join(binary_strings)
    # original binary sequence
    binary_sequence = combined_binary_string

    len_of_bs = len(binary_sequence)

    group_size = codec.AD
    padding_numbers = group_size - len_of_bs % codec.bacl.get_available_digits()
    # we need extra padding_numbers' zeros

    binary_sequence = binary_sequence + "0" * padding_numbers
    last_padding_char = codec.padding_dict[padding_numbers]


    ret_seq = []
    groups = [
        binary_sequence[i : i + group_size]
        for i in range(0, len(binary_sequence), group_size)
    ]

    # if the last group is not complete, we need to add padding
    for u in groups:
        ret_seq.append(codec.bacl[int(u, 2)])
    if padding_numbers != 0:
        ret_seq.append(last_padding_char)
    return "".join(ret_seq)
