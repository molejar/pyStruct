#!/usr/bin/env python

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

from os import path
from setuptools import setup
from easy_struct import __version__, __license__, __author__, __contact__


def get_long_description():
    with open(path.join(path.dirname(path.abspath(__file__)), 'README.md'), encoding='utf8') as fp:
        return fp.read()


setup(
    name='easy_struct',
    version=__version__,
    license=__license__,
    author=__author__,
    author_email=__contact__,
    url='https://github.com/molejar/pyStruct',
    description='User friendly implementation of C-like structure type in Python',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    packages=['easy_struct'],
    python_requires=">=3.5",
    setup_requires=[
        'setuptools>=40.0'
    ],
    install_requires=[
        'easy_enum==0.3.0'
    ],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        'Topic :: Utilities'
    ]
)
