from basechinese.encoder import encode
from basechinese.decoder import decode
print(encode(b"Hello, World!"))
hw = "妃邦右盏复迂罚找岔卫益"  # the result of encode(b"Hello, World!")
print(decode(hw))

from baseany.baseany import anyencode, anydecode

r = anyencode(b"Hello, World!", mode="CPN")
print(r)
print(anydecode(r))