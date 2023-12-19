import baseany
import os
bacl = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), # src
    'bacl.txt', # bacl
)
with open(bacl, 'r', encoding="utf8") as f:
    cp = f.read()

baseany.CODE_PAGE = cp

source = b"Hello World!"

ret = baseany.anyencode(source)

r = baseany.anydecode(ret)

if r != source:
    raise Exception(repr(r) + " != " + repr(source))

