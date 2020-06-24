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

from jinja2 import Template

output_file = "../easy_struct/help_types.py"
template_file = "help_types.j2"


def gen_int_items():
    data = []

    sizes = (8, 16, 24, 32, 64)
    marks = {'u': 'False', 's': 'True'}
    endians = ('little', 'big')

    for size in sizes:
        for mark, mark_value in marks.items():
            name = "Int{}{}".format(size, mark)
            args = "{}, {}".format(size//8, mark_value)
            data.append({'class_name': name, 'args': args})

    for mark, mark_value in marks.items():
        for endian in endians:
            for size in sizes[1:]:
                name = "Int{}{}{}".format(size, mark, endian[0])
                args = "{}, {}, '{}'".format(size//8, mark_value, endian)
                data.append({'class_name': name, 'args': args})

    return data


def gen_float_items():
    data = []

    sizes = (16, 32, 64)
    endians = ('little', 'big')

    for endian in endians:
        for size in sizes:
            name = "Float{}{}".format(size, endian[0])
            args = "{}, '{}'".format(size//8, endian)
            data.append({'class_name': name, 'args': args})

    return data


if __name__ == "__main__":

    input_data = {
        'int_items': gen_int_items(),
        'float_items': gen_float_items()
    }

    with open(template_file, 'r') as file:
        template = file.read()

    output_data = Template(template).render(input_data)

    with open(output_file, 'w') as f:
        f.write(output_data)

