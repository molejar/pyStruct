# Copyright 2019 Martin Olejar
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional, Union, Any
from struct import unpack_from, pack
from easy_enum import Enum


########################################################################################################################
# The Integer Bitfield Type as Item for DataStructure
########################################################################################################################
class IntBits:

    class_type = int

    __slots__ = ('bits', 'endian', 'default', 'signed', 'offset', 'min_value', 'max_value', 'choices', 'print_format',
                 'name', 'description')

    def __init__(self, bits: int, offset: int = 0, default=0, endian: str = 'little', signed: bool = False,
                 min: Optional[int] = None, max: Optional[int] = None, choices: Any = None,
                 pfmt: Optional[str] = None, name: Optional[str] = None, desc: Optional[str] = None) -> None:

        assert bits > 0
        assert endian in ('big', 'little')
        assert isinstance(signed, bool)

        self.name = name
        self.bits = bits
        self.endian = endian
        self.signed = signed
        self.offset = offset
        self.choices = None
        self.print_format = pfmt
        self.min_value = -(1 << (bits - 1)) if signed else 0
        self.max_value = (1 << (bits - 1)) - 1 if signed else (1 << bits) - 1
        self.description = desc

        if min is not None:
            if self.min_value <= min <= self.max_value:
                self.min_value = min
            else:
                raise Exception()

        if min is not None:
            if self.min_value <= max <= self.max_value:
                self.max_value = max
            else:
                raise Exception()

        if choices is not None:
            if isinstance(choices, (tuple, list)):
                self.choices = [self.validate(v) for v in choices]
            elif isinstance(choices, type) and issubclass(choices, Enum):
                for item in choices:
                    try:
                        self.validate(item[1])
                    except ValueError as e:
                        raise ValueError("choices: {}".format(str(e)))

                self.choices = choices
            else:
                raise Exception()

        self.default = self.validate(default)

    @property
    def size(self) -> int:
        return self.bits

    def encode(self, value: int) -> int:
        mask = (1 << self.bits) - 1
        return (value & mask) << self.offset

    def decode(self, value: int) -> int:
        mask = (1 << self.bits) - 1
        ret_val = (value >> self.offset) & mask
        return (ret_val ^ (1 << (self.bits - 1))) - (1 << (self.bits - 1)) if self.signed else ret_val

    def pack(self, value: int) -> bytes:
        raise NotImplemented()

    def unpack(self, data: bytes, offset: int = 0) -> int:
        raise NotImplemented()

    def validate(self, value: int) -> int:
        if not isinstance(value, int):
            raise TypeError("The value type is '{}' and must be 'int'".format(type(value).__name__))

        if self.choices is None:
            if self.min_value is not None and value < self.min_value:
                raise ValueError()

            if self.max_value is not None and value > self.max_value:
                raise ValueError()

        else:
            if value not in self.choices:
                raise ValueError()

        return value


########################################################################################################################
# The Integer Type in Bytes as Item for DataStructure
########################################################################################################################
class Int:

    class_type = int

    __slots__ = ('bytes', 'endian', 'default', 'signed', 'offset', 'min_value', 'max_value', 'choices', 'constant',
                 'print_format', 'name', 'description')

    def __init__(self, bytes: int, signed: bool = False, endian: str = 'little', default=0, offset: int = 0,
                 min: Optional[int] = None, max: Optional[int] = None, choices: Any = None,
                 pfmt: Optional[str] = None, name: Optional[str] = None, desc: Optional[str] = None) -> None:

        assert endian in ('big', 'little')
        assert isinstance(signed, bool)

        self.name = name
        self.bytes = bytes
        self.endian = endian
        self.signed = signed
        self.offset = offset
        self.choices = None
        self.print_format = pfmt
        self.min_value = -(1 << ((bytes * 8) - 1)) if signed else 0
        self.max_value = (1 << ((bytes * 8) - 1)) - 1 if signed else (1 << (bytes * 8)) - 1
        self.description = desc

        if min is not None:
            if self.min_value <= min <= self.max_value:
                self.min_value = min
            else:
                raise Exception()

        if min is not None:
            if self.min_value <= max <= self.max_value:
                self.max_value = max
            else:
                raise Exception()

        if choices is not None:
            if isinstance(choices, (tuple, list)):
                self.choices = [self.validate(v) for v in choices]
            elif isinstance(choices, type) and issubclass(choices, Enum):
                for item in choices:
                    self.validate(item[1])
                self.choices = choices
                if self.description is None:
                    self.description = self.choices.__doc__
            else:
                raise Exception()

        self.default = self.validate(default)

    @property
    def size(self) -> int:
        return self.bytes

    def pack(self, value: int) -> bytes:
        return value.to_bytes(self.bytes, self.endian, signed=self.signed)

    def unpack(self, data: bytes, offset: int = 0) -> int:
        return int.from_bytes(data[offset: offset + self.bytes], self.endian, signed=self.signed)

    def validate(self, value: int) -> int:
        if not isinstance(value, int):
            raise TypeError("The value type is '{}' and must be 'int'".format(type(value).__name__))

        if self.choices is None:
            if self.min_value is not None and value < self.min_value:
                raise ValueError()

            if self.max_value is not None and value > self.max_value:
                raise ValueError()

        else:
            if value not in self.choices:
                raise ValueError()

        return value


########################################################################################################################
# The Float Type in Bytes as Item for DataStructure
########################################################################################################################
class Float:

    class_type = float

    __slots__ = ('bytes', 'endian', 'default', 'offset', 'min_value', 'max_value', 'choices', 'print_format',
                 'name', 'description')

    def __init__(self, bytes: int, endian: str, default: float, offset: int = 0,
                 min: Optional[float] = None, max: Optional[float] = None, choices: Any = None,
                 pfmt: Optional[str] = None, name: Optional[str] = None, desc: Optional[str] = None) -> None:

        assert bytes in (2, 4, 8)
        assert endian in ('big', 'little')

        self.name = name
        self.bytes = bytes
        self.endian = endian
        self.offset = offset
        self.choices = None
        self.print_format = pfmt
        self.min_value = min
        self.max_value = max
        self.description = desc

        if choices is not None:
            if not isinstance(choices, (tuple, list)):
                raise Exception("The choices type is '{}' and must be 'tuple' or 'list'".format(type(choices).__name__))

            self.choices = [self.validate(v) for v in choices]

        self.default = self.validate(default)

    @property
    def size(self) -> int:
        return self.bytes

    def pack(self, value: float) -> bytes:
        fmt = {'little': '<', 'big': '>'}[self.endian]
        fmt += {2: 'e', 4: 'f', 8: 'd'}[self.bytes]
        return pack(fmt, value)

    def unpack(self, data: bytes, offset: int = 0) -> float:
        fmt = {'little': '<', 'big': '>'}[self.endian]
        fmt += {2: 'e', 4: 'f', 8: 'd'}[self.bytes]
        return unpack_from(fmt, data, offset)[0]

    def validate(self, value: float) -> float:
        if not isinstance(value, float):
            raise TypeError()

        if self.choices is None:
            if self.min_value is not None and value < self.min_value:
                raise ValueError()

            if self.max_value is not None and value > self.max_value:
                raise ValueError()

        else:
            if value not in self.choices:
                raise ValueError()

        return value


########################################################################################################################
# The String Type as Item for DataStructure
########################################################################################################################
class String:

    class_type = str

    __slots__ = ('length', 'default', 'offset', 'empty', 'encoding', 'choices', 'name', 'description')

    def __init__(self, length: int, default: str = '', offset: int = 0, empty: str = '\0', encoding: str = 'ascii',
                 choices: Optional[list] = None, name: Optional[str] = None, desc: Optional[str] = None) -> None:

        assert isinstance(empty, str) and len(empty) == 1
        assert encoding in ('ascii', 'utf-8', 'utf-16', 'utf-16-be', 'utf-16-le')

        self.name = name
        self.empty = empty
        self.length = length
        self.offset = offset
        self.encoding = encoding
        self.choices = None
        self.description = desc

        if choices is not None:
            if not isinstance(choices, (tuple, list)):
                raise Exception()
            self.choices = [self.validate(v) for v in choices]

        if self.choices is not None and isinstance(default, int):
            self.default = self.choices[default]
        elif isinstance(default, str):
            self.default = self.validate(default)
        else:
            raise Exception()

    @property
    def size(self) -> int:
        return self.length * (1 if self.encoding in ('ascii', 'utf-8') else 2)

    def pack(self, value: str) -> bytes:
        str_value = value
        if len(value) < self.length:
            str_value += self.empty * (self.length - len(value))
        return str_value.encode(self.encoding)

    def unpack(self, data: bytes, offset: int = 0) -> str:
        return data[offset: offset + self.size].decode(self.encoding).strip('\0').strip()

    def validate(self, value: str) -> str:
        if not isinstance(value, str):
            raise TypeError()

        if len(value) > self.length:
            raise ValueError()

        if self.choices is not None and value not in self.choices:
            raise ValueError()

        return value


########################################################################################################################
# The Bytes Type as Item for DataStructure
########################################################################################################################
class Bytes:

    class_type = (bytes, bytearray)

    __slots__ = ('size', 'empty', 'offset', 'default',  'name', 'description')

    def __init__(self, size: int, empty: int = 0, offset: int = 0, default: Union[bytes, bytearray, None] = None,
                 name: Optional[str] = None, desc: Optional[str] = None) -> None:

        self.name = name
        self.size = size
        self.empty = empty
        self.offset = offset
        self.default = self.validate(default) if default is not None else default
        self.description = desc

    def pack(self, value: bytearray) -> bytes:
        return bytes(value)

    def unpack(self, data: bytes, offset: int = 0) -> bytearray:
        return bytearray(data[offset: offset + self.size])

    def validate(self, value: Union[bytes, bytearray]) -> bytearray:
        if not isinstance(value, (bytes, bytearray)):
            raise TypeError()

        if len(value) != self.size:
            raise ValueError()

        return value if isinstance(value, bytearray) else bytearray(value)


########################################################################################################################
# The Array Type as Item for DataStructure
########################################################################################################################
class Array:

    class_type = list

    __slots__ = ('item_type', 'length', 'offset', 'default', 'name', 'description')

    def __init__(self, itype, length: Union[int, str], offset: int = 0, default: Optional[list] = None,
                 name: Optional[str] = None, desc: Optional[str] = None) -> None:

        assert isinstance(itype, (Int, Float, String)) or issubclass(itype, (Int, Float, String))

        self.name = name
        self.item_type = itype() if isinstance(itype, type) else itype
        self.length = length
        self.offset = offset
        self.description = desc

        if default is None:
            self.default = [self.item_type.default for _ in range(length)] if isinstance(length, int) else []
        elif isinstance(default, list):
            self.default = self.validate(default)
        else:
            raise Exception()

    @property
    def size(self) -> int:
        return self.item_type.size * self.length if isinstance(self.length, int) else None

    def pack(self, values: list) -> bytes:
        return b''.join(self.item_type.pack(v) for v in values)

    def unpack(self, data: bytes, offset: int = 0) -> list:
        values = []
        for i in range(self.length):
            values.append(self.item_type.unpack(data, offset))
            offset += self.item_type.size
        return values

    def validate(self, values: list) -> list:
        if not isinstance(values, list):
            raise TypeError()

        if len(values) != self.length:
            raise ValueError()

        for item in values:
            self.item_type.validate(item)

        return values


########################################################################################################################
# The Custom Int Type as Item for DataStructure
########################################################################################################################
class CInt:
    pass
