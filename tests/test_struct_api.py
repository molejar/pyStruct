
import pytest
from easy_enum import Enum
from easy_struct import *


class ImageType(Enum):
    """ U-Boot Image Type """

    STANDALONE = (1, "standalone", "Standalone Program")
    KERNEL = (2, "kernel", "Kernel Image")
    RAMDISK = (3, "ramdisk", "RAMDisk Image")
    MULTI = (4, "multi", "Multi-File Image")
    FIRMWARE = (5, "firmware", "Firmware Image")
    SCRIPT = (6, "script", "U-Boot Script Image")
    FILESYSTEM = (7, "filesystem", "Filesystem Image")
    FLATDT = (8, "flat-dt", "Flat Device Tree Image")


class DSClassic(DataStructure):
    """ Example of DataStructure using classic syntax """

    signature = Int32ul(default=0x155729, pfmt='X', desc="Description of signature")
    image_type = Int8u(default=ImageType.STANDALONE, choices=ImageType)
    image_size = Int32ul(default=1280000, pfmt='Z')
    _reserved0 = Int16ul(name="reserved", desc="Reserved for later usage")
    data = Bytes(length=100, empty=0x0F, name='raw_data', desc="Description of data item")
    items = Array(itype=Int32sl, length=5, offset=5, default=[0, 1, 2, 3, -10000000])


class DSAttributes(DataStructure):
    """ Example of DataStructure using attributes syntax """

    signature:  Int32ul(default=0x155729, pfmt='X', desc="Description of signature")
    image_type: Int8u(default=ImageType.STANDALONE, choices=ImageType)
    image_size: Int32ul(default=1280000, pfmt='Z')
    _reserved0: Int16ul(name="reserved", desc="Reserved for later usage")
    data:       Bytes(length=100, empty=0x0F, name='raw_data', desc="Description of data item")
    items:      Array(itype=Int32sl, length=5, offset=5, default=[0, 1, 2, 3, -10000000])


def test_compare():
    dsc = DSClassic()
    dsa = DSAttributes()
    assert dsa == dsc


def test_data_structure():
    ds = DSClassic(signature=0x55555555)
    assert ds.signature == 0x55555555
    assert ds.image_type == ImageType.STANDALONE
    assert ds.image_size == 1280000

    assert ds.raw_size() == 136
    assert ds.info()

    data = ds.export()
    assert len(data) == 136
