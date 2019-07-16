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

from easy_struct.items import *
from easy_struct.core import *

__author__  = "Martin Olejar"
__contact__ = "martin.olejar@gmail.com"
__version__ = "0.1.1"
__license__ = "Apache 2.0"
__status__  = "Development"

__all__ = [
    "DataStructure",
    "Struct",
    "String",
    "Bytes",
    "Array",
    "Int"
]
__all__ += [f"Int{n}{us}{bl}" for n in (8, 16, 24, 32, 64) for us in "us" for bl in "bl"]
__all__ += [f"Float{n}{bl}" for n in (16, 32, 64) for bl in "bl"]
