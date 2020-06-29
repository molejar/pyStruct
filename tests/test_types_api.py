
import pytest
from easy_struct import *


def test_int_bits_type():
    value = IntBits(bits=6, offset=4, default=5, signed=True)
    assert value.class_type is int
    assert value.offset == 4
    assert value.default == 5
    # validator test
    assert value.validate(-5)
    with pytest.raises(TypeError):
        value.validate('0')
    with pytest.raises(ValueError):
        value.validate(-100)
    with pytest.raises(ValueError):
        value.validate(100)
    # pack test
    assert value.encode(5) == 5 << 4
    # unpack test
    assert value.decode(0b1010000) == 5


def test_int_type():
    value = Int(bytes=2, endian='little', default=10, min=1, max=2000)
    assert value.class_type is int
    assert value.bytes == 2
    assert value.endian == 'little'
    assert value.default == 10
    assert value.size == 2
    # validator test
    assert value.validate(5)
    with pytest.raises(TypeError):
        value.validate('0')
    with pytest.raises(ValueError):
        value.validate(0)
    with pytest.raises(ValueError):
        value.validate(20001)
    # pack test
    assert value.pack(5) == b'\x05\x00'
    # unpack test
    assert value.unpack(b'\x05\x00') == 5


def test_float_type():
    value = Float(bytes=2, endian='little', default=1.0, min=0.1, max=10.0)
    assert value.class_type is float
    assert value.bytes == 2
    assert value.endian == 'little'
    assert value.default == 1.0
    # validator test
    assert value.validate(0.5)
    with pytest.raises(TypeError):
        value.validate(0)
    with pytest.raises(ValueError):
        value.validate(0.01)
    with pytest.raises(ValueError):
        value.validate(10.1)
    # pack test
    assert value.pack(1.0) == b'\x00<'
    # unpack test
    assert value.unpack(b'\x00<') == 1.0


def test_string_type():
    value = String(length=10, default='example', encoding='utf-8', empty='\0')
    assert value.class_type is str
    assert value.length == 10
    assert value.default == 'example'
    assert value.encoding == 'utf-8'
    assert value.size == 10
    # validator test
    assert value.validate('test')
    with pytest.raises(TypeError):
        value.validate(0)
    with pytest.raises(ValueError):
        value.validate("12345678901")
    # pack test
    assert value.pack("0123456789") == b'0123456789'
    assert value.pack("012345") == b'012345\x00\x00\x00\x00'
    # unpack test
    assert value.unpack(b'0123456789') == "0123456789"
    assert value.unpack(b'012345\x20\x00\x00\x00') == "012345"


def test_bytes_type():
    value = Bytes(length=10)
    assert value.class_type == (bytes, bytearray)
    assert value.size == 10
    # validator test
    assert value.validate(b'\0' * 10)
    with pytest.raises(TypeError):
        value.validate(0)
    with pytest.raises(ValueError):
        value.validate(b'\0' * 8)
    # pack test
    assert value.pack(bytearray(b'0123456')) == b'0123456'
    # unpack test
    assert value.unpack(b'0123456789') == bytearray(b'0123456789')


def test_array_type():
    value = Array(Int16ul, length=10)
    assert value.class_type is list
    assert isinstance(value.item_type, Int16ul)
    assert value.length == 10
    assert value.size == 20
    # validator test
    assert value.validate([5, 10, 58, 800, 1500, 8000, 20, 70, 100, 1587])
    with pytest.raises(TypeError):
        value.validate(0)
    with pytest.raises(ValueError):
        value.validate([5, 10, 58, -800, 1500, 8000, 20, 70, 100, 1587])
    with pytest.raises(ValueError):
        value.validate([5, 10, 58, 800])
