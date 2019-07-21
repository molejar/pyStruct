
import pytest
from easy_struct import *


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
    # pack test
    assert value.pack(5) == b'\x05\x00'
    # unpack test
    assert value.unpack(b'\x05\x00') == 5


def test_float_type():
    value = Float(bytes=2, endian='little', default=1.0)
    assert value.class_type is float
    assert value.bytes == 2
    assert value.endian == 'little'
    assert value.default == 1.0
    # validator test
    assert value.validate(0.5)
    with pytest.raises(TypeError):
        value.validate(0)
    # pack test
    # unpack test


def test_string_type():
    value = String(length=10, default='example', encoding='utf-8')
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
    # assert value.pack(5) == b'\x05\x00'
    # unpack test
    # assert value.unpack(b'\x05\x00') == 5


def test_bytes_type():
    value = Bytes(size=10)
    assert value.class_type == (bytes, bytearray)
    assert value.size == 10
    # validator test
    assert value.validate(b'\0' * 10)
    with pytest.raises(TypeError):
        value.validate(0)
    with pytest.raises(ValueError):
        value.validate(b'\0' * 8)


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
