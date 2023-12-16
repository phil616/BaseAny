import unittest
import baseany

class TestBaseAny(unittest.TestCase):
    """
    TestBaseAny class provide some basic testcase for baseany module.
    """
    CONST = b'Hello World'
    CODEPAGE = "0123456789"
    def test_encode(self):
        baseany.CODE_PAGE = self.CODEPAGE
        encode = baseany.anyencode(self.CONST)
        decode = baseany.anydecode(encode)
        self.assertEqual(decode, self.CONST)
    def test_duplication_exception(self):
        with self.assertRaises(baseany.DuplicationException):
            baseany.CODE_PAGE = self.CODEPAGE+'0'
            baseany.anyencode(self.CONST)
    def test_invalid_length_exception(self):
        with self.assertRaises(baseany.InvaildLengthException):
            baseany.CODE_PAGE = "012345678"
            baseany.anyencode(self.CONST)