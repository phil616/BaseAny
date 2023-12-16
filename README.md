# BaseAny

A project to convert any characters and binary data to and from each other. like base64

## be advised

due to the fuzzy logic, module `basechinese` is not recommended 

## Usage

```python
from basechinese.encoder import encode
from basechinese.decoder import decode
print(encode(b"Hello, World!"))
hw = "妃邦右盏复迂罚找岔卫益"  # the result of encode(b"Hello, World!")
print(decode(hw))
```

## Usage of BaseAny

```python
from baseany.baseany import anyencode, anydecode

r = anyencode(b"Hello, World!", mode="CPN")
print(r)
print(anydecode(r))
```

## LICENSE

Apache License 2.0

## TODOs

- [x] Add more tests
- [ ] form a package
- [x] add more docs
- [ ] calculate compression ratio
- [ ] host resources to other platforms

## References

- [Base64](https://en.wikipedia.org/wiki/Base64)
- [Base85](https://en.wikipedia.org/wiki/Ascii85)
