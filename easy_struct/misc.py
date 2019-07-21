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


def loff(offset, tabsize, string):
    return str(" " * (tabsize * offset)) + string


def size_fmt(num, kibibyte=True):
    base, suffix = [(1000., 'B'), (1024., 'iB')][kibibyte]
    for x in ['B'] + [x + suffix for x in list('kMGTP')]:
        if -base < num < base:
            break
        num /= base

    return "{} {}".format(num, x) if x == 'B' else "{:3.2f} {}".format(num, x)


def fmt_int(name, metadata, value, tabsize=4, offset=0):

    raw_value = value & (1 << (metadata.bytes * 8)) - 1 if value < 0 else value

    if metadata.print_format in ('x', 'X'):
        fmt = "{{}}: 0x{{:0{}{}}}".format(metadata.bytes * 2, metadata.print_format)
        msg = loff(offset, tabsize, fmt.format(name, raw_value))
    elif metadata.print_format in ('o', 'O'):
        msg = loff(offset, tabsize, "{}: 0{:o}".format(name, raw_value))
    elif metadata.print_format in ('b', 'B'):
        fmt = "{{}}: 0b{{:0{}b}}".format(metadata.bytes * 8)
        msg = loff(offset, tabsize, fmt.format(name, raw_value))
    elif metadata.print_format in ('sz', 'SZ'):
        msg = loff(offset, tabsize, "{}: {} / {}".format(name, value, size_fmt(value, metadata.print_format == 'sz')))
    else:
        msg = loff(offset, tabsize, "{}: {}".format(name, value))

    if isinstance(metadata.choices, type) and issubclass(metadata.choices, Enum):
        msg += " / {}.{}".format(metadata.choices.__name__, metadata.choices[value])

    return msg + '\n'


def fmt_bytes(name, metadata, data, tabsize=4, offset=0, line_size=16):

    if len(data) < 16**4:
        fmt = "{{:04X}} | {{:<{}s}} | {{}}\n".format(3 * line_size - 1)
    elif len(data) < 16**8:
        fmt = "{{:08X}} | {{:<{}s}} | {{}}\n".format(3 * line_size - 1)
    else:
        raise ValueError("hexdump cannot process more than 16**8 or 4294967296 bytes")

    msg = loff(offset, tabsize, "{}[{}]:\n".format(name, len(data)))
    for i in range(0, len(data), line_size):
        hex_text = " ".join(format(c, '02X') for c in data[i: i + line_size])
        raw_text = "".join(chr(c) if 32 <= c < 128 else '.' for c in data[i: i + line_size])
        msg += loff(offset + 1, tabsize, fmt.format(i, hex_text, raw_text))

    return msg


def fmt_array(name, metadata, data, tabsize=4, offset=0):

    msg = str()
    msg += loff(offset, tabsize, "{}[{} * {}]:\n".format(name, len(data), metadata.item_type.__class__.__name__))
    msg += loff(offset + 1, tabsize, "{}\n".format(data))

    return msg


def fmt_string(name, metadata, value, tabsize=4, offset=0):

    msg = loff(offset, tabsize, "{}: \"{}\"\n".format(name, value))

    return msg
