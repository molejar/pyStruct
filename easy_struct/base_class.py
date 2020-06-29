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
from easy_struct.base_types import IntBits, Int, Float, String, Array, Bytes
from typing import Optional, Union, Any


########################################################################################################################
# Helper functions for base DataStructure
########################################################################################################################
def loff(offset: int, tabsize: int, string: str) -> str:
    return str(" " * (tabsize * offset)) + string


def prefix(offset: int, tabsize: int, name: str, align: int) -> str:
    return str(" " * (tabsize * offset)) + name + ': ' + str(" " * (align - len(name)))


def size_fmt(num: int, kibibyte: bool = True) -> str:
    base, suffix = [(1000., 'B'), (1024., 'iB')][kibibyte]
    for x in ['B'] + [x + suffix for x in list('kMGTP')]:
        if -base < num < base:
            break
        num /= base
    return "{} {}".format(num, x) if x == 'B' else "{:3.2f} {}".format(num, x)


def fmt_int(name: str, metadata: Any, value: int, tabsize: int, offset: int, align: int) -> str:
    if not isinstance(value, int):
        return prefix(offset, tabsize, name, align) + str(value) + "\n"
    bits = metadata.bits if hasattr(metadata, 'bits') else metadata.bytes * 8
    raw_value = value & ((1 << bits) - 1) if value < 0 else value
    if metadata.print_format in ('x', 'X'):
        fmt = "0x{{:0{}{}}}".format(bits // 4, metadata.print_format)
        msg = prefix(offset, tabsize, name, align) + fmt.format(raw_value)
    elif metadata.print_format in ('o', 'O'):
        msg = prefix(offset, tabsize, name, align) + "0{:o}".format(raw_value)
    elif metadata.print_format in ('b', 'B'):
        fmt = "0b{{:0{}b}}".format(bits)
        msg = prefix(offset, tabsize, name, align) + fmt.format(name, raw_value)
    elif metadata.print_format in ('z', 'Z'):
        msg = prefix(offset, tabsize, name, align)
        msg += "{} ({})".format(value, size_fmt(value, metadata.print_format == 'z'))
    else:
        msg = prefix(offset, tabsize, name, align) + str(value)
    if isinstance(metadata.choices, type) and issubclass(metadata.choices, Enum):
        # msg += " ({}[{}])".format(metadata.choices.__name__, metadata.choices[value])
        msg += " ({})".format(metadata.choices[value])
    return msg + '\n'


def fmt_bytes(name: str, metadata: Any, data: bytearray, tabsize: int = 4, offset: int = 0, line_size: int = 16) -> str:
    if len(data) >= (16 ** 8):
        raise ValueError("hexdump cannot process more than 16**8 or 4294967296 bytes")
    fmt = "{{:0{}X}} | {{:<{}s}} | {{}}\n".format(4 if len(data) < (16 ** 4) else 8, 3 * line_size - 1)
    msg = loff(offset, tabsize, "{}[{}]:\n".format(name, len(data)))
    for i in range(0, len(data), line_size):
        hex_text = " ".join(format(c, '02X') for c in data[i: i + line_size])
        raw_text = "".join(chr(c) if 32 <= c < 128 else '.' for c in data[i: i + line_size])
        msg += loff(offset + 1, tabsize, fmt.format(i, hex_text, raw_text))
        if i > line_size * 10:
            msg += loff(offset + 1, tabsize, "...\n")
            break
    return msg


def fmt_array(name: str, metadata: Any, data: list, tabsize: int = 4, offset: int = 0) -> str:
    msg = str()
    msg += loff(offset, tabsize, "{}[{} * {}]:\n".format(name, len(data), metadata.item_type.__class__.__name__))
    msg += loff(offset + 1, tabsize, "{}\n".format(data))
    return msg


def fmt_string(name: str, metadata: Any, value: str, tabsize: int, offset: int, align: int) -> str:
    msg = prefix(offset, tabsize, name, align) + "\"{}\"\n".format(value)
    return msg


########################################################################################################################
# Metaclass for base DataStructure
########################################################################################################################
class MetaStructure(type):
    """ MetaClass for Structure Type """

    def __new__(mcs, name, bases, ns, endian=None):
        if name != 'DataStructure':
            if '__annotations__' in ns:
                for key, value in ns['__annotations__'].items():
                    if isinstance(value, type):
                        value = ns['__annotations__'][key] = value()
                    if not isinstance(value, (Struct, Int, IntBits, Float, String, Bytes, Array)):
                        raise Exception()
                    if endian and isinstance(value, (Int, Float)):
                        value.endian = endian
                    # create class attribute with default value
                    ns[key] = value.default

            else:
                annotations = {}
                for key, value in ns.items():
                    # ignore hidden class attributes
                    if key in set(dir(type(name, (object,), {}))) or (key.startswith('_') and key.endswith('_')):
                        continue
                    # ignore methods and properties
                    if isinstance(value, type(Struct.validate)) or isinstance(value, staticmethod) or \
                       isinstance(value, classmethod) or isinstance(value, property):
                        continue
                    # convert class to objects
                    if isinstance(value, type):
                        value = value()
                    if not isinstance(value, (Struct, Int, IntBits, String, Bytes, Array)):
                        raise Exception()
                    annotations[key] = value
                    ns[key] = value.default

                ns['__annotations__'] = annotations

        return super().__new__(mcs, name, bases, ns)


########################################################################################################################
# The base DataStructure class
########################################################################################################################
class DataStructure(metaclass=MetaStructure):

    def __init__(self, **kwargs):
        """

        """
        for name, metadata in getattr(self.__class__, '__annotations__', {}).items():
            if name in kwargs:
                value = metadata.validate(kwargs[name])
            else:
                value = metadata.default
                if isinstance(metadata, Bytes) and value is None:
                    value = bytearray([metadata.empty] * metadata.size)

            self.__dict__[name] = value

    def __getitem__(self, key):
        if not isinstance(key, str):
            raise KeyError()

        for name, metadata in getattr(self.__class__, '__annotations__', {}).items():
            if metadata.name == key:
                key = name
                break

        if key not in self.__dict__:
            raise KeyError()

        return getattr(self, key)

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise KeyError()

        for name, metadata in getattr(self.__class__, '__annotations__', {}).items():
            if metadata.name == key:
                key = name
                break

        if key not in self.__dict__:
            raise KeyError()

        setattr(self, key, value)

    def __setattr__(self, key, value):
        if key in self.__dict__:
            annotations = getattr(self.__class__, '__annotations__')
            self.__dict__[key] = annotations[key].validate(value)
        else:
            prop_obj = getattr(self.__class__, key, None)
            if isinstance(prop_obj, property):
                if prop_obj.fset is None:
                    raise AttributeError("Property '{}' has not implemented setter".format(key))
                prop_obj.fset(self, value)

            else:
                # super(DataStructure, self).__setattr__(key, value)
                raise AttributeError("Add new attribute into object is forbidden")

    def __contains__(self, key):
        return True if isinstance(key, str) and key in self.__dict__.keys() else False

    def __iter__(self):
        return self.__dict__.__iter__()

    def __len__(self):
        return len(self.__dict__)

    def __eq__(self, obj):
        if not isinstance(obj, DataStructure):
            return False

        for key, value in self.__dict__.items():
            if key not in obj or value != obj[key]:
                return False

        return True

    def update(self):
        """ Update exporting data

        Implement in child class if need do some changes before export
        """
        pass

    def validate(self):
        """ Validate parsed data

        Implement in child class if need do validate parsed data
        """
        pass

    def raw_size(self) -> int:
        size = 0
        index = 0
        bsize = 0

        items = getattr(self.__class__, '__annotations__', {})
        names = tuple(items.keys())

        while index < len(items):
            name = names[index]
            mdata = items[name]
            index += 1

            if isinstance(mdata, IntBits) and bsize < (mdata.offset + mdata.bits):
                bsize = mdata.offset + mdata.bits
                if index < len(items):
                    continue

            if bsize > 0:
                size += (bsize // 8) + 1 if bsize % 8 else bsize // 8
                bsize = 0
                continue

            size += mdata.offset
            if isinstance(mdata, Struct):
                value = getattr(self, name)
                size += value.raw_size()
            if isinstance(mdata, Bytes):
                value = getattr(self, name)
                size += len(value)
            else:
                size += mdata.size

        return size

    def info(self, tabsize: int = 4, offset: int = 0, align: int = 0, show_all: bool = False) -> str:
        """
        :param tabsize:
        :param offset:
        :param align:
        :param show_all:
        :return:
        """
        self.update()

        msg = str()
        if self.__doc__:
            msg += loff(offset, tabsize, '[ ' + self.__doc__ + ' ]\n')

        for name, metadata in getattr(self.__class__, '__annotations__', {}).items():
            value = getattr(self, name)
            if name.startswith('_'):
                name = name.lstrip('_')
                if not hasattr(self, name) and not show_all:
                    continue

            if metadata.name:
                name = metadata.name
            if metadata.description is not None:
                msg += loff(offset, tabsize, "# {}\n".format(metadata.description))
            if hasattr(metadata, 'print_format') and callable(metadata.print_format):
                msg += metadata.print_format(name, value, tabsize, offset, align)

            else:
                if isinstance(metadata, Struct):
                    msg += loff(offset, tabsize, "{}:\n".format(name))
                    msg += value.info(tabsize, offset + 1, align, show_all)
                elif isinstance(metadata, Array):
                    msg += fmt_array(name, metadata, value, tabsize, offset)
                elif isinstance(metadata, Bytes):
                    msg += fmt_bytes(name, metadata, value, tabsize, offset)
                elif isinstance(metadata, Int):
                    msg += fmt_int(name, metadata, value, tabsize, offset, align)
                elif isinstance(metadata, IntBits):
                    msg += fmt_int(name, metadata, value, tabsize, offset, align)
                else:
                    msg += fmt_string(name, metadata, value, tabsize, offset, align)

        return msg

    def export(self, empty: int = 0x00, update: bool = True, ignore: Optional[list] = None) -> bytes:
        """
        :param empty:
        :param update:
        :param ignore:
        :return:
        """
        assert 0 <= empty <= 0xFF

        index = 0
        raw_data = b''
        ib_range = 0
        ib_values = []
        ib_mdatas = []

        items = getattr(self.__class__, '__annotations__', {})
        if ignore:
            items = {k: v for k, v in items.items() if k not in ignore}
        names = tuple(items.keys())

        if update:
            self.update()

        while index < len(items):
            name = names[index]
            mdata = items[name]
            value = getattr(self, name)
            index += 1

            if isinstance(mdata, IntBits):
                ib_values.append(value)
                ib_mdatas.append(mdata)
                if ib_range < (mdata.offset + mdata.bits):
                    ib_range = mdata.offset + mdata.bits
                if index < len(items):
                    continue

            if ib_values:
                length = (ib_range // 8) + 1 if ib_range % 8 else ib_range // 8
                raw_value = 0
                for i, m in enumerate(ib_mdatas):
                    raw_value |= m.encode(ib_values[i])
                raw_data += raw_value.to_bytes(length=length, byteorder='little', signed=False)
                ib_range = 0
                ib_values = []
                ib_mdatas = []

            else:
                raw_data += bytes([empty] * mdata.offset)
                raw_data += value.export(empty, update) if isinstance(mdata, Struct) else mdata.pack(value)

        return raw_data

    @classmethod
    def parse(cls, data: bytes, offset: int = 0):
        """
        :param data:
        :param offset:
        :return:
        """
        if len(data) <= offset:
            raise Exception()

        index = 0
        kwargs = {}
        ib_range = 0
        ib_names = []
        ib_mdatas = []

        items = cls.__annotations__
        names = tuple(items.keys())

        while index < len(items):
            name = names[index]
            mdata = items[name]
            index += 1

            if isinstance(mdata, IntBits):
                ib_names.append(name)
                ib_mdatas.append(mdata)
                if ib_range < (mdata.offset + mdata.bits):
                    ib_range = mdata.offset + mdata.bits
                if index < len(items):
                    continue

            if ib_range:
                length = (ib_range // 8) + 1 if ib_range % 8 else ib_range // 8
                raw_value = int.from_bytes(data[offset: offset + length], byteorder='little', signed=False)
                for i, m in enumerate(ib_mdatas):
                    kwargs[ib_names[i]] = m.decode(raw_value)
                offset += length

            else:
                offset += mdata.offset
                if isinstance(mdata, Struct):
                    value = mdata.struct.parse(data, offset)
                    offset += value.raw_size()
                elif isinstance(mdata, Bytes):
                    length = mdata.length
                    if isinstance(length, str):
                        il = kwargs
                        for m in mdata.length.split('.'):
                            if not il or m not in il:
                                raise Exception()
                            il = il[m]
                        length = il
                        
                    value = bytearray(data[offset: offset + length])
                    offset += length
                else:
                    value = mdata.unpack(data, offset)
                    offset += mdata.size

                kwargs[name] = value

        obj = cls(**kwargs)
        obj.validate()
        return obj


########################################################################################################################
# The Struct Type as DataStructure container
########################################################################################################################
class Struct:
    __slots__ = ('struct', 'offset', 'name', 'description')

    def __init__(self, struct: MetaStructure, offset: int = 0, name: Optional[str] = None, desc: Optional[str] = None):

        assert issubclass(struct, DataStructure)

        self.name = name
        self.offset = offset
        self.struct = struct
        self.description = desc

    @property
    def default(self):
        return self.struct()

    def validate(self, value):
        if not isinstance(value, self.struct):
            raise TypeError()

        return value
