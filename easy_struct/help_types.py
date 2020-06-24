# Copyright 2020 Martin Olejar
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

from easy_struct.base_types import Int, Float


########################################################################################################################
# The Integer Types used as items in DataStructure
########################################################################################################################

class Int8u(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(1, False, **kwargs)


class Int8s(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(1, True, **kwargs)


class Int16u(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(2, False, **kwargs)


class Int16s(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(2, True, **kwargs)


class Int24u(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(3, False, **kwargs)


class Int24s(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(3, True, **kwargs)


class Int32u(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(4, False, **kwargs)


class Int32s(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(4, True, **kwargs)


class Int64u(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(8, False, **kwargs)


class Int64s(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(8, True, **kwargs)


class Int16ul(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(2, False, 'little', **kwargs)


class Int24ul(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(3, False, 'little', **kwargs)


class Int32ul(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(4, False, 'little', **kwargs)


class Int64ul(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(8, False, 'little', **kwargs)


class Int16ub(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(2, False, 'big', **kwargs)


class Int24ub(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(3, False, 'big', **kwargs)


class Int32ub(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(4, False, 'big', **kwargs)


class Int64ub(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(8, False, 'big', **kwargs)


class Int16sl(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(2, True, 'little', **kwargs)


class Int24sl(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(3, True, 'little', **kwargs)


class Int32sl(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(4, True, 'little', **kwargs)


class Int64sl(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(8, True, 'little', **kwargs)


class Int16sb(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(2, True, 'big', **kwargs)


class Int24sb(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(3, True, 'big', **kwargs)


class Int32sb(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(4, True, 'big', **kwargs)


class Int64sb(Int):
    def __init__(self, **kwargs) -> None:
        super().__init__(8, True, 'big', **kwargs)


########################################################################################################################
# The Float Types used as items in DataStructure
########################################################################################################################

class Float16l(Float):
    def __init__(self, **kwargs) -> None:
        super().__init__(2, 'little', **kwargs)


class Float32l(Float):
    def __init__(self, **kwargs) -> None:
        super().__init__(4, 'little', **kwargs)


class Float64l(Float):
    def __init__(self, **kwargs) -> None:
        super().__init__(8, 'little', **kwargs)


class Float16b(Float):
    def __init__(self, **kwargs) -> None:
        super().__init__(2, 'big', **kwargs)


class Float32b(Float):
    def __init__(self, **kwargs) -> None:
        super().__init__(4, 'big', **kwargs)


class Float64b(Float):
    def __init__(self, **kwargs) -> None:
        super().__init__(8, 'big', **kwargs)


ALL_HELPER_TYPES = [

    # Integer Types
    "Int8u",
    "Int8s",
    "Int16u",
    "Int16s",
    "Int24u",
    "Int24s",
    "Int32u",
    "Int32s",
    "Int64u",
    "Int64s",
    "Int16ul",
    "Int24ul",
    "Int32ul",
    "Int64ul",
    "Int16ub",
    "Int24ub",
    "Int32ub",
    "Int64ub",
    "Int16sl",
    "Int24sl",
    "Int32sl",
    "Int64sl",
    "Int16sb",
    "Int24sb",
    "Int32sb",
    "Int64sb",
    
    # Float Types
    "Float16l",
    "Float32l",
    "Float64l",
    "Float16b",
    "Float32b",
    "Float64b",
    
]