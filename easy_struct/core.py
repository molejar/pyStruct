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

from easy_struct.misc import *
from easy_struct.items import *


class Struct:
    __slots__ = ('struct', 'offset', 'default', 'name', 'description')

    def __init__(self, struct, default=None, offset=0, name=None, desc=None):
        assert issubclass(struct, DataStructure)
        self.name = name
        self.offset = offset
        self.struct = struct
        if default is None:
            self.default = struct()
        elif isinstance(default, struct):
            self.default = default
        else:
            raise Exception()
        self.description = desc

    def validate(self, value):
        if not isinstance(value, self.struct):
            raise TypeError()

        return value


class MetaStructure(type):
    """ MetaClass for Structure Type """

    def __new__(mcs, name, bases, ns):
        if '__annotations__' in ns:
            for key, value in ns['__annotations__'].items():
                if isinstance(value, type):
                    value = ns['__annotations__'][key] = value()
                if not isinstance(value, (Struct, Int, String, Bytes, Array)):
                    raise Exception()

                # create class attribute with default value
                ns[key] = value.default

        return super().__new__(mcs, name, bases, ns)


class DataStructure(metaclass=MetaStructure):

    def __init__(self, **kwargs):
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

        if key in self.__dict__:
            return getattr(self, key)

        raise KeyError()

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise KeyError()

        for name, metadata in getattr(self.__class__, '__annotations__', {}).items():
            if metadata.name == key:
                key = name
                break

        if key in self.__dict__:
            setattr(self, key, value)
        else:
            raise KeyError()

    def __setattr__(self, key, value):
        # week attributes are forbidden
        if key not in self.__dict__:
            raise AttributeError()

        # get annotations from class
        annotations = getattr(self.__class__, '__annotations__')
        # set new validated value for specified attribute
        self.__dict__[key] = annotations[key].validate(value)

    def __iter__(self):
        return self.__dict__.__iter__()

    def __len__(self):
        return len(self.__dict__)

    def update(self):
        # implement in child class if need do some changes before export
        pass

    def raw_size(self):
        size = 0
        for name, metadata in getattr(self.__class__, '__annotations__', {}).items():
            size += metadata.offset
            if isinstance(metadata, Struct):
                value = getattr(self, name)
                size += value.raw_size()
            else:
                size += metadata.size
        return size

    def info(self, tabsize=4, offset=0):
        """
        :param tabsize:
        :param offset:
        :return:
        """
        msg = str()
        self.update()
        for name, metadata in getattr(self.__class__, '__annotations__', {}).items():
            value = getattr(self, name)
            if metadata.name is not None:
                name = metadata.name
            if metadata.description is not None:
                msg += loff(offset, tabsize, "# {}\n".format(metadata.description))
            if isinstance(metadata, Struct):
                msg += loff(offset, tabsize, "{}:\n".format(name))
                msg += value.info(tabsize, offset + 1)
            elif isinstance(metadata, Array):
                msg += fmt_array(name, metadata, value, tabsize, offset)
            elif isinstance(metadata, Bytes):
                msg += fmt_bytes(name, metadata, value, tabsize, offset)
            elif isinstance(metadata, Int):
                msg += fmt_int(name, metadata, value, tabsize, offset)
            else:
                msg += fmt_string(name, metadata, value, tabsize, offset)
        return msg

    def export(self, empty=0x00):
        """
        :param empty:
        :return:
        """
        raw_data = b''
        self.update()
        for name, metadata in getattr(self.__class__, '__annotations__', {}).items():
            value = getattr(self, name)
            raw_data += bytes([0] * metadata.offset)
            raw_data += value.export(empty) if isinstance(metadata, Struct) else metadata.pack(value)

        return raw_data

    @classmethod
    def parse(cls, data, offset=0):
        """
        :param data:
        :param offset:
        :return:
        """
        if len(data) <= offset:
            raise Exception()

        kwargs = {}
        for name, metadata in cls.__annotations__.items():
            offset += metadata.offset
            if isinstance(metadata, Struct):
                value = metadata.struct.parse(data, offset)
                offset += value.raw_size()
            else:
                value = metadata.unpack(data, offset)
                offset += metadata.size

            kwargs[name] = value

        return cls(**kwargs)



