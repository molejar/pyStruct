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

from easy_struct.items import Int, Float, String, Bytes, Array
from easy_struct.items import Int8ul, Int8sl, Int8ub, Int8sb, Int16ul, Int16sl, Int16ub, Int16sb, Int24ul, Int24sl, \
                              Int24ub, Int24sb, Int32ul, Int32sl, Int32ub, Int32sb, Int64ul, Int64sl, Int64ub, Int64sb
from easy_struct.items import Float16l, Float16b, Float32l, Float32b, Float64l, Float64b
from easy_struct.core import DataStructure, Struct

__author__  = "Martin Olejar"
__contact__ = "martin.olejar@gmail.com"
__version__ = "0.0.1"
__license__ = "Apache 2.0"
__status__  = "Development"
__all__ = [
    "DataStructure",
    "Struct",
    "String",
    "Bytes",
    "Array",
    "Float",
    "Int",
    # Int variants
    'Int8ul',
    'Int8sl',
    'Int8ub',
    'Int8sb',
    'Int16ul',
    'Int16sl',
    'Int16ub',
    'Int16sb',
    'Int24ul',
    'Int24sl',
    'Int24ub',
    'Int24sb',
    'Int32ul',
    'Int32sl',
    'Int32ub',
    'Int32sb',
    'Int64ul',
    'Int64sl',
    'Int64ub',
    'Int64sb',
    # Float variants
    'Float16l',
    'Float16b',
    'Float32l',
    'Float32b',
    'Float64l',
    'Float64b'
]
