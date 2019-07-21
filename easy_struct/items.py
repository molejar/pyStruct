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

from easy_enum import Enum


########################################################################################################################
# Integer Type in Bits
########################################################################################################################

class IntBits:

    class_type = int

    __slots__ = ('bits', 'endian', 'default', 'signed', 'offset', 'min_value', 'max_value', 'choices',
                 'print_format', 'name', 'description')

    def __init__(self, bits, endian, default, signed=False, offset=0, min=None, max=None, choices=None, pfmt=None,
                 name=None, desc=None):

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
                    self.validate(item[1])
                self.choices = choices
            else:
                raise Exception()

        self.default = self.validate(default)

    @property
    def size(self):
        return (self.offset + self.bits) // 8

    def pack(self, value):
        return 0

    def unpack(self, data, offset):
        return 0

    def validate(self, value):
        if not isinstance(value, int):
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
# Integer Type in Bytes
########################################################################################################################

class Int:

    class_type = int

    __slots__ = ('bytes', 'endian', 'default', 'signed', 'offset', 'min_value', 'max_value', 'choices',
                 'print_format', 'name', 'description')

    def __init__(self, bytes, endian, default=0, signed=False, offset=0, min=None, max=None, choices=None, pfmt=None,
                 name=None, desc=None):

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
    def size(self):
        return self.bytes

    def pack(self, value):
        return value.to_bytes(self.bytes, self.endian, signed=self.signed)

    def unpack(self, data, offset=0):
        return int.from_bytes(data[offset: offset + self.bytes], self.endian, signed=self.signed)

    def validate(self, value):
        if not isinstance(value, int):
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


class Int8ul(Int):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt=None, name=None, desc=None):
        super().__init__(1, 'little', default, False, offset, min, max, choices, pfmt, name, desc)


class Int16ul(Int):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt=None, name=None, desc=None):
        super().__init__(2, 'little', default, False, offset, min, max, choices, pfmt, name, desc)


class Int24ul(Int):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt=None, name=None, desc=None):
        super().__init__(3, 'little', default, False, offset, min, max, choices, pfmt, name, desc)


class Int32ul(Int):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt=None, name=None, desc=None):
        super().__init__(4, 'little', default, False, offset, min, max, choices, pfmt, name, desc)


class Int64ul(Int):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt=None, name=None, desc=None):
        super().__init__(8, 'little', default, False, offset, min, max, choices, pfmt, name, desc)


class Int8ub(Int):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt=None, name=None, desc=None):
        super().__init__(1, 'big', default, False, offset, min, max, choices, pfmt, name, desc)


class Int16ub(Int):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt=None, name=None, desc=None):
        super().__init__(2, 'big', default, False, offset, min, max, choices, pfmt, name, desc)


class Int24ub(Int):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt=None, name=None, desc=None):
        super().__init__(3, 'big', default, False, offset, min, max, choices, pfmt, name, desc)


class Int32ub(Int):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt=None, name=None, desc=None):
        super().__init__(4, 'big', default, False, offset, min, max, choices, pfmt, name, desc)


class Int64ub(Int):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt=None, name=None, desc=None):
        super().__init__(8, 'big', default, False, offset, min, max, choices, pfmt, name, desc)


class Int8sl(Int):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt=None, name=None, desc=None):
        super().__init__(1, 'little', default, True, offset, min, max, choices, pfmt, name, desc)


class Int16sl(Int):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt=None, name=None, desc=None):
        super().__init__(2, 'little', default, True, offset, min, max, choices, pfmt, name, desc)


class Int24sl(Int):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt=None, name=None, desc=None):
        super().__init__(3, 'little', default, True, offset, min, max, choices, pfmt, name, desc)


class Int32sl(Int):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt=None, name=None, desc=None):
        super().__init__(4, 'little', default, True, offset, min, max, choices, pfmt, name, desc)


class Int64sl(Int):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt=None, name=None, desc=None):
        super().__init__(8, 'little', default, False, offset, min, max, choices, pfmt, name, desc)


class Int8sb(Int):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt=None, name=None, desc=None):
        super().__init__(1, 'big', default, True, offset, min, max, choices, pfmt, name, desc)


class Int16sb(Int):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt=None, name=None, desc=None):
        super().__init__(2, 'big', default, True, offset, min, max, choices, pfmt, name, desc)


class Int24sb(Int):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt=None, name=None, desc=None):
        super().__init__(3, 'big', default, True, offset, min, max, choices, pfmt, name, desc)


class Int32sb(Int):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt=None, name=None, desc=None):
        super().__init__(4, 'big', default, True, offset, min, max, choices, pfmt, name, desc)


class Int64sb(Int):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt=None, name=None, desc=None):
        super().__init__(8, 'big', default, False, offset, min, max, choices, pfmt, name, desc)


########################################################################################################################
# Float Type in Bytes
########################################################################################################################

class Float:

    class_type = float

    __slots__ = ('bytes', 'endian', 'default', 'offset', 'min_value', 'max_value', 'choices', 'print_format',
                 'name', 'description')

    def __init__(self, bytes, endian, default, offset=0, min=None, max=None, choices=None, pfmt=None, name=None,
                 desc=None):

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
                raise Exception()

            self.choices = [self.validate(v) for v in choices]

        self.default = self.validate(default)

    @property
    def size(self):
        return self.bytes

    def pack(self, value):
        pass

    def unpack(self, data, offset=0):
        pass

    def validate(self, value):
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


class Float16l(Float):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt='d', name=None, desc=None):
        super().__init__(2, 'little', default, offset, min, max, choices, pfmt, name, desc)


class Float32l(Float):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt='d', name=None, desc=None):
        super().__init__(4, 'little', default, offset, min, max, choices, pfmt, name, desc)


class Float64l(Float):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt='d', name=None, desc=None):
        super().__init__(8, 'little', default, offset, min, max, choices, pfmt, name, desc)


class Float16b(Float):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt='d', name=None, desc=None):
        super().__init__(2, 'big', default, offset, min, max, choices, pfmt, name, desc)


class Float32b(Float):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt='d', name=None, desc=None):
        super().__init__(4, 'big', default, offset, min, max, choices, pfmt, name, desc)


class Float64b(Float):
    def __init__(self, default=0, offset=0, min=None, max=None, choices=None, pfmt='d', name=None, desc=None):
        super().__init__(8, 'big', default, offset, min, max, choices, pfmt, name, desc)


########################################################################################################################
# String Type
########################################################################################################################

class String:

    class_type = str

    __slots__ = ('length', 'default', 'offset', 'empty', 'encoding', 'choices', 'name', 'description')

    def __init__(self, length, default='', offset=0, empty=' ', encoding='ascii', choices=None, name=None, desc=None):
        assert encoding in ('ascii', 'utf-8', 'utf-16', 'utf-16-be', 'utf-16-le')
        self.name = name
        self.empty = empty
        self.length = length
        self.offset = offset
        self.encoding = encoding
        self.choices = None
        self.description = desc
        if choices is not None:
            if isinstance(choices, (tuple, list)):
                self.choices = [self.validate(v) for v in choices]
            else:
                raise Exception()

        if self.choices is not None and isinstance(default, int):
            self.default = self.choices[default]
        elif isinstance(default, str):
            self.default = self.validate(default)
        else:
            raise Exception()



    @property
    def size(self):
        char_size = {'ascii': 1, 'utf-8': 1, 'utf-16': 2, 'utf-16-be': 2, 'utf-16-le': 2}
        return self.length * char_size[self.encoding]

    def pack(self, value):
        if len(value) < self.length:
            str_value = value + (self.empty * (self.length - len(value)))
        else:
            str_value = value
        return str_value.encode(self.encoding)

    def unpack(self, data, offset=0):
        return data[offset: offset + self.size].decode(self.encoding).strip()

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError()

        if len(value) > self.length:
            raise ValueError()

        if self.choices is not None and value not in self.choices:
            raise ValueError()

        return value


########################################################################################################################
# Bytes Array Type
########################################################################################################################

class Bytes:

    class_type = (bytes, bytearray)

    __slots__ = ('size', 'empty', 'offset', 'default',  'name', 'description')

    def __init__(self, size, empty=0, offset=0, default=None, name=None, desc=None):
        self.name = name
        self.size = size
        self.empty = empty
        self.offset = offset
        self.default = self.validate(default) if default is not None else default
        self.description = desc

    def pack(self, value):
        return bytes(value)

    def unpack(self, data, offset=0):
        return bytearray(data[offset: offset + self.size])

    def validate(self, value):
        if not isinstance(value, (bytes, bytearray)):
            raise TypeError()

        if len(value) != self.size:
            raise ValueError()

        return bytearray(value) if isinstance(value, bytes) else value


########################################################################################################################
# Universal Array Type
########################################################################################################################

class Array:

    class_type = list

    __slots__ = ('item_type', 'length', 'offset', 'default', 'name', 'description')

    def __init__(self, itype, length, offset=0, default=None, name=None, desc=None):
        assert isinstance(itype, (Int, Float, String)) or issubclass(itype, (Int, Float, String))
        self.name = name
        self.item_type = itype() if isinstance(itype, type) else itype
        self.length = length
        self.offset = offset
        self.description = desc
        if default is None:
            self.default = [self.item_type.default for _ in range(length)]
        elif isinstance(default, list):
            self.default = self.validate(default)
        else:
            raise Exception()

    @property
    def size(self):
        return self.item_type.size * self.length

    def pack(self, value):
        raw_data = bytes()
        for v in value:
            raw_data += self.item_type.pack(v)
        return raw_data

    def unpack(self, data, offset=0):
        values = []
        for i in range(self.length):
            values.append(self.item_type.unpack(data, offset))
            offset += self.item_type.size
        return values

    def validate(self, value):
        if not isinstance(value, list):
            raise TypeError()

        if len(value) != self.length:
            raise ValueError()

        for item in value:
            self.item_type.validate(item)

        return value
