from basechinese.codec import load_info
from basechinese.exceptions import InputTypeException

def decode(char_data:str)->bytes:

    if not isinstance(char_data,str):
        raise InputTypeException("The input data should be str")
    codec = load_info()
    reverse_dict = codec.bacl.get_reverse_dict()
    int_sequence = [reverse_dict[c] for c in char_data]
    reverse_padding_dict = {v:k for k,v in codec.padding_dict.items()}
    print("reverse_padding_dict",reverse_padding_dict)
    padding_char = codec.bacl[int_sequence[-1]]


    if padding_char in codec.padding_dict.values():
        padding_zeros = reverse_padding_dict[padding_char]
        int_sequence.pop()
        # there is a padding exist

    binary_strings = [format(x,f'0{codec.AD}b') for x in int_sequence]
    binary_string = "".join(binary_strings)
    trimmed_str = binary_string[:-padding_zeros] if padding_zeros > 0 else binary_string

    # turn str to int value
    int_value = int(trimmed_str, 2)

    # confirm how may 
    num_bytes = (len(trimmed_str) + 7) // 8

    # convert num_bytes to bytes_value
    bytes_value = int_value.to_bytes(num_bytes, byteorder='big')
    return bytes_value