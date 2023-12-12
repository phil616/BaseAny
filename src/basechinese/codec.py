


from basechinese.bacl import BACL
import os

SRC_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACL_PATH = os.path.join(SRC_PATH,"bacl.txt")

class Codec:
    AD:int
    PC:int
    padding_dict:dict
    bacl:BACL
    def __init__(self,AD:int,PC:int,padding_dict:dict,bacl:BACL):
        self.AD = AD
        self.PC = PC
        self.padding_dict = padding_dict
        self.bacl = bacl

def load_info(path:os.PathLike=None)->Codec:
    if path is None:
        path = BACL_PATH
    with open(path, "r", encoding="utf8") as f:
        data = f.read()
    bacl = BACL(data)
    AD = bacl.get_available_digits()
    PC = bacl.get_padding_chars_number()
    padding_dict = bacl.get_padding_chars()
    padding_count = 0
    formatted_padding_dict = {}
    for _,v in padding_dict.items():
        formatted_padding_dict.update({padding_count+1:v})
        padding_count+=1
    return Codec(
        AD=AD,
        PC=PC,
        padding_dict=formatted_padding_dict,
        bacl=bacl
    )