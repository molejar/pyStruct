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

from os import path
from zlib import crc32
from typing import Union, Any
from datetime import datetime
from easy_enum import Enum
from easy_struct import DataStructure, Int8u, Int32u, String, Bytes, Struct, prefix


########################################################################################################################
# Enums
########################################################################################################################

class EnumImageType(Enum):
    """Supported UBoot Image Types"""

    STANDALONE = (1, "standalone", "Standalone Program")
    KERNEL = (2, "kernel", "Kernel Image")
    RAMDISK = (3, "ramdisk", "RAMDisk Image")
    MULTI = (4, "multi", "Multi-File Image")
    FIRMWARE = (5, "firmware", "Firmware Image")
    SCRIPT = (6, "script", "U-Boot Script Image")
    FILESYSTEM = (7, "filesystem", "Filesystem Image")
    FLATDT = (8, "flat_dt", "Flat Device Tree Image")
    KWB = (9, "kwbimage", "Kirkwood Boot Image")
    IMX = (10, "imximage", "Freescale i.MX Boot Image")
    UBL = (11, "ublimage", "Davinci UBL image")
    OMAP = (12, "omapimage", "TI OMAP SPL With GP CH")
    AIS = (13, "aisimage", "Davinci AIS image")
    KNOLOAD = (14, "kernel_noload", "Kernel Image (no loading done)")
    PBL = (15, "pblimage", "Freescale PBL Boot Image")
    MXS = (16, "mxsimage", "Freescale MXS Boot Image")
    GP = (17, "gpimage", "TI Keystone SPL Image")
    ATMEL = (18, "atmelimage", "ATMEL ROM-Boot Image")
    SOCFPGA = (19, "socfpgaimage", "Altera SOCFPGA preloader")
    X86SETUP = (20, "x86_setup", "x86 setup.bin")
    LPC32XX = (21, "lpc32xximage", "LPC32XX Boot Image")
    LOADABLE = (22, "loadable", "A list of typeless images")
    RKBOOT = (23, "rkimage", "Rockchip Boot Image")
    RKSD = (24, "rksd", "Rockchip SD Boot Image")
    RKSPI = (25, "rkspi", "Rockchip SPI Boot Image")
    ZYNQ = (26, "zynqimage", "Xilinx Zynq Boot Image")
    ZYNQMP = (27, "zynqmpimage", "Xilinx ZynqMP Boot Image")
    FPGA = (28, "fpga", "FPGA Image")
    VYBRID = (29, "vybridimage", "Vybrid Boot Image")
    TEE = (30, "tee", "Trusted Execution Environment Image")
    FW_IVT = (31, "firmware_ivt", "Firmware with HABv4 IVT")
    PMMC = (32, "pmmc", "TI Power Management Micro-Controller Firmware")


class EnumOsType(Enum):
    """Supported Operating Systems"""

    OPENBSD = (1, "openbsd", "OpenBSD")
    NETBSD = (2, "netbsd", "NetBSD")
    FREEBSD = (3, "freebsd", "FreeBSD")
    BSD4 = (4, "4-4bsd", "4-4BSD")
    LINUX = (5, "linux", "Linux")
    SVR4 = (6, "svr4", "SVR4")
    ESIX = (7, "esix", "Esix")
    SOLARIS = (8, "solaris", "Solaris")
    IRIX = (9, "irix", "Irix")
    SCO = (10, "sco", "SCO")
    DELL = (11, "dell", "Dell")
    NCR = (12, "ncr", "NCR")
    LYNXOS = (13, "lynxos", "LynxOS")
    VXWORKS = (14, "vxworks", "VxWorks")
    PSOS = (15, "psos", "pSOS")
    QNX = (16, "qnx", "QNX")
    UBOOT = (17, "u-boot", "U-Boot Firmware")
    RTEMS = (18, "rtems", "RTEMS")
    ARTOS = (19, "artos", "ARTOS")
    UNITY = (20, "unity", "Unity OS")
    INTEGRITY = (21, "integrity", "INTEGRITY")
    OSE = (22, "ose", "Enea OSE")
    PLAN9 = (23, "plan9", "Plan 9")
    OPENRTOS = (24, "openrtos", "OpenRTOS")


class EnumArchType(Enum):
    """Supported CPU Architectures"""

    ALPHA = (1, "alpha", "Alpha")
    ARM = (2, "arm", "ARM")
    I386 = (3, "x86", "Intel x86")
    IA64 = (4, "ia64", "IA64")
    MIPS = (5, "mips", "MIPS")
    MIPS64 = (6, "mips64", "MIPS 64-Bit")
    PPC = (7, "powerpc", "PowerPC")
    S390 = (8, "s390", "IBM S390")
    SH = (9, "sh", "SuperH")
    SPARC = (10, "sparc", "SPARC")
    SPARC64 = (11, "sparc64", "SPARC 64 Bit")
    M68K = (12, "m68k", "M68K")
    NIOS = (13, "nios", "Nios 32")
    MICROBLAZE = (14, "microblaze", "MicroBlaze")
    NIOS2 = (15, "nios2", "NIOS II")
    BLACKFIN = (16, "blackfin", "Blackfin")
    AVR32 = (17, "avr32", "AVR32")
    ST200 = (18, "ST200", "STMicroelectronics ST200")
    SANDBOX = (19, "sandbox", "Sandbox architecture (test only)")
    NDS32 = (20, "nds32", "ANDES Technology - NDS32")
    OPENRISC = (21, "or1k", "OpenRISC 1000")
    ARM64 = (22, "arm64", "AArch64")
    ARC = (23, "arc", "Synopsis DesignWare ARC")
    X86_64 = (24, "x86_64", "AMD x86_64, Intel and Via")
    XTENSA = (25, "xtensa", "Xtensa")


class EnumCompressionType(Enum):
    """Supported Data Compression"""

    NONE = (0, 'none', 'Uncompressed')
    GZIP = (1, 'gzip', 'Compressed with GZIP')
    BZIP2 = (2, 'bzip2', 'Compressed with BZIP2')
    LZMA = (3, 'lzma', 'Compressed with LZMA')
    LZO = (4, 'lzo', 'Compressed with LZO')
    LZ4 = (5, 'lz4', 'Compressed with LZ4')


########################################################################################################################
# Helper functions
########################################################################################################################

def timestamp_print(name: str, value: Any, tabsize: int, offset: int, align: int) -> str:
    info = prefix(offset, tabsize, name, align)
    info += datetime.fromtimestamp(value).strftime("%H:%M:%S (%d.%m.%Y)")
    info += "\n"
    return info


########################################################################################################################
# U-boot image data structure with isolated header
########################################################################################################################

class ImgHeader(DataStructure, endian='little'):
    # """The Header of U-boot Executable Image"""

    # private (hidden) attributes
    _magic_number: Int32u(default=0x27051956, choices=[0x27051956], pfmt='X')
    _header_crc:   Int32u(pfmt='X')
    _timestamp:    Int32u(pfmt=timestamp_print)

    # public attributes
    data_size:     Int32u(pfmt='Z')
    load_address:  Int32u(pfmt='X')
    entry_address: Int32u(pfmt='X')
    data_crc:      Int32u(pfmt='X', desc="The CRC of data section")
    os_type:       Int8u(default=EnumOsType.LINUX, choices=EnumOsType)
    arch_type:     Int8u(default=EnumArchType.ARM, choices=EnumArchType)
    image_type:    Int8u(default=EnumImageType.FIRMWARE, choices=EnumImageType)
    compression:   Int8u(default=EnumCompressionType.NONE, choices=EnumCompressionType)
    image_name:    String(length=32, default="U-Boot Executable Image")

    @property
    def timestamp(self) -> datetime:
        return datetime.fromtimestamp(self._timestamp)

    @timestamp.setter
    def timestamp(self, value: Union[int, datetime]):
        assert isinstance(value, (int, datetime))
        self._timestamp = value if isinstance(value, int) else int(value.timestamp())

    def update(self):
        self._header_crc = 0
        self._header_crc = crc32(self.export(update=False))

    def validate(self):
        pars_crc = self._header_crc
        self._header_crc = 0
        calc_crc = crc32(self.export(update=False))
        if pars_crc != calc_crc:
            raise Exception("Invalid Header CRC")


class Img(DataStructure):
    """U-boot Executable Image"""

    header: Struct(ImgHeader)
    data:   Bytes(length='header.data_size')

    def update(self):
        self.header.data_crc = crc32(self.data)
        self.header.data_size = len(self.data)

    def validate(self):
        if self.header.data_crc != crc32(self.data):
            raise Exception("Invalid Data CRC")


########################################################################################################################
#  U-boot image data structure as single container
########################################################################################################################

class UImage(DataStructure, endian='little'):
    """U-boot Executable Image"""

    # Image Header
    _magic_number: Int32u(default=0x27051956, choices=[0x27051956], pfmt='X')  # hidden private attribute as constant
    _header_crc:   Int32u(pfmt='X')                                            # hidden private attribute
    _timestamp:    Int32u(pfmt=timestamp_print)                                # hidden attribute with public interface
    data_size:     Int32u(pfmt='Z')                                            # public attribute
    load_address:  Int32u(pfmt='X')
    entry_address: Int32u(pfmt='X')
    data_crc:      Int32u(pfmt='X', desc="The CRC of data section")
    os_type:       Int8u(default=EnumOsType.LINUX, choices=EnumOsType)
    arch_type:     Int8u(default=EnumArchType.ARM, choices=EnumArchType)
    image_type:    Int8u(default=EnumImageType.FIRMWARE, choices=EnumImageType)
    compression:   Int8u(default=EnumCompressionType.NONE, choices=EnumCompressionType)
    image_name:    String(length=32, default="U-Boot Executable Image")

    # Image Data (the length is specified in header)
    image_data:    Bytes(length='data_size')

    @property
    def timestamp(self) -> datetime:
        return datetime.fromtimestamp(self._timestamp)

    @timestamp.setter
    def timestamp(self, value: Union[int, datetime]):
        assert isinstance(value, (int, datetime))
        self._timestamp = value if isinstance(value, int) else int(value.timestamp())

    def update(self):
        self.data_crc = crc32(self.image_data)
        self.data_size = len(self.image_data)
        self._header_crc = 0
        self._header_crc = crc32(self.export(update=False, ignore=['image_data']))

    def validate(self):
        pars_crc = self._header_crc
        self._header_crc = 0
        calc_crc = crc32(self.export(update=False, ignore=['image_data']))
        if pars_crc != calc_crc:
            raise Exception("Invalid Header CRC")
        if self.data_crc != crc32(self.image_data):
            raise Exception("Invalid Data CRC")


########################################################################################################################
# The main code (usage)
########################################################################################################################

if __name__ == "__main__":

    # update to existing u-boot file name
    image_file = "file.bin"

    if path.exists(image_file):
        with open(image_file, 'rb') as f:
            data = f.read()
            # parse1
            img_obj = Img.parse(data)
            print(img_obj.info(show_all=True))
            # parse2
            img_obj = UImage.parse(data)
            print(img_obj.info(show_all=True))

    else:
        # create image instance
        img_obj = UImage(entry_address=0x80000, image_data=b'0'*160)
        # use property for set timestamp in datetime
        img_obj.timestamp = datetime(year=2020, month=6, day=12, hour=22)
        # print image info
        print(img_obj.info(show_all=True))
        # export as bytes array
        data = img_obj.export()

        # parse and print info
        img = Img.parse(data)
        print(img.info(show_all=True))
        # export as bytes array
        data2 = img.export()
        # compare data
        print(data == data2)

        # use instance check for enable autocomplete in IDE
        if isinstance(img.header, ImgHeader):
            img.header.load_address = 5
            img.header.timestamp = datetime(year=2020, month=6, day=12, hour=2)

        # extend data
        img.data += b'12345678'
        print(img.info(align=13))
