pyStruct
========

User friendly implementation of C-like structure type in Python language.

Dependencies
------------

- [Python](https://www.python.org) - Python 3.x interpreter
- [easy_enum](https://github.com/molejar/pyEnum) - User friendly implementation of documented Enum type for Python language.

Installation
------------

To install the latest version from master branch execute in shell following commands:

``` bash
    $ pip install -U https://github.com/molejar/pyStruct/archive/master.zip
```

In case of development, install pyEnum from sources:

``` bash
    $ git clone https://github.com/molejar/pyStruct.git
    $ cd pyStruct
    $ pip install -U -e .
```

You may run into a permissions issues running these commands. Here are a few options how to fix it:

1. Run with `sudo` to install pyStruct and dependencies globally
2. Specify the `--user` option to install locally into your home directory (export "~/.local/bin" into PATH variable if haven't).
3. Run the command in a [virtualenv](https://virtualenv.pypa.io/en/latest/) local to a specific project working set.

Usage
-----

Example code:

``` Python
    import re
    from easy_enum import EEnum as Enum
    from easy_struct import *

    class MyEnum(Enum):
        """ Example of Enum """
        ITEM1 = (1, 'first', 'Description for first item')   
        ITEM2 = (2, 'second', 'Description for second item')
        ITEM3 = (3, 'third', 'Description for third item')
        ITEM4 = (4, 'fourth', 'Description for fourth item')
    
    class MyStruct(DataStructure):
        """ Example of Data Structure """
    
        # public member with string type
        name: String(14, default="example string")
        
        # private members with 16-bit unsigned little endian type
        _major_version: Int16ul
        _minor_version: Int16ul
        
        # others public members
        flags: Int8ul(MyEnum.ITEM2, opt=MyEnum)
        user_id: Int16ul(0xF0F125D, fmt='X')
        
        # reserved bytes can be defined as private member or skipt with offset parameter
        # _reserved: Int32ul
        temperature: Int8sl(22, min=-20, max=100, offset=4)
        
        # bytes array
        data: Bytes(24)
    
        @property
        def version(self):
            return f"{self._major_version}.{self._minor_version}"

        @version.setter
        def version(self, value):
            assert isinstance(value, str) and re.match(r'^\d+\.\d+$, value)
            self._major_version, self._minor_version = [int(v) for v in value.split('.')]
        
        # user methods
        # ...
        
    if __name__ == '__main__':
        # main code
        ms = MyStruct()
        print(ms.info())
        data = ms.export()
        parsed_ms = MyStruct.parse(data)
        print(parsed_ms.info())
```
