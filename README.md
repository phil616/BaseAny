# BaseChinese

A project to convert Chinese characters and binary data to and from each other.

In theory, this project can convert any character set into binary encoding, not limited to Chinese characters. Just replace bacl to achieve any encoding.

## Usage

```python
from basechinese.encoder import encode
from basechinese.decoder import decode
print(encode(b"Hello, World!"))
hw = "妃邦右盏复迂罚找岔卫益"  # the result of encode(b"Hello, World!")
print(decode(hw))
```
## LICENSE

Apache License 2.0

## TODOs

- [ ] Add more tests
- [ ] form a package
- [ ] add more docs
- [ ] calculate compression ratio
- [ ] host resources to other platforms

## References

- [Base64](https://en.wikipedia.org/wiki/Base64)
- [Base85](https://en.wikipedia.org/wiki/Ascii85)
