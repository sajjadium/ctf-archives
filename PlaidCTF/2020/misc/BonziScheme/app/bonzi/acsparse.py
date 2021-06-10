import os
import struct
from tabulate import tabulate
import numpy as np
import bitstring
from PIL import Image


SZ_ULONG    = 4
SZ_LONG     = 4
SZ_USHORT   = 2
SZ_SHORT    = 2
SZ_BYTE     = 1
SZ_WCHAR    = 2


class ACSParseException(Exception):
    def __init__(self, value):
        super(ACSParseException, self).__init__()
        self._value = value
    
    def __str__(self):
        return f"ACSParseException: {self._value}"


class ACS(object):
    def __init__(self, buf, offset):
        self._buf = buf
        self._offset = offset
        self._size = 0

    def unpack_data(self, format):
        res = struct.unpack_from(format, self._buf, offset=self._offset+self._size)
        self._size += struct.calcsize(format)
        return res

    def unpack_struct(self, ClassType, *argv):
        if argv == ():
            res = ClassType(self._buf, self._offset+self._size)
        else:
            res = ClassType(self._buf, self._offset+self._size, *argv)
        self._size += res.get_size()
        return res

    def unpack_chunk(self, size):
        res = self._buf[self._offset+self._size:self._offset+self._size+size]
        self._size += size
        return res

    def get_size(self):
        return self._size

    def get_offset(self):
        return self._offset

# ====================

class ACSHeader(ACS):
    # Bonz says no

        
class ACSLocator(ACS):
    # Bonz says no


class ACSList(ACS):
    # Bonz says no


class ACSCharacterInfo(ACS):
    # Bonz says no
    

class TrayIcon(ACS):
    # Bonz says no


class IconImage(ACS):
    # Bonz says no


class BitmapInfoHeader(ACS):
    # Bonz says no


class Guid(ACS):
    # Bonz says no


class LocalizedInfo(ACS):
    # Bonz says no


class VoiceInfo(ACS):
    # Bonz says no


class BalloonInfo(ACS):
    # Bonz says no


class PaletteColor(ACS):
    # Bonz says no


class StateInfo(ACS):
    # Bonz says no


class LangID(ACS):
    # Bonz says no


class String(ACS):
    # Bonz says no


class RGBQuad(ACS):
    # Bonz says no


class ACSAnimationInfo(ACS):
    # Bonz says no


class ACSImageInfo(ACS):
    # Bonz says no


class ACSAudioInfo(ACS):
    # Bonz says no


class DataBlock(ACS):
    # Bonz says no


class ImageInfo(ACS):
    # Bonz says no

    # But then bonz says yes
    def bytes_to_bitstream(self, data_bytes):
        data_bitstream = bitstring.BitArray(data_bytes)
        for i in range(0, len(data_bitstream), 8):
            data_bitstream.reverse(i, i+8)
        return data_bitstream

    def bitstream_to_bytes(self, data_bitstream, offset, length):
        data_bytes = data_bitstream[offset:offset+length]
        for i in range(0, len(data_bytes), 8):
            data_bytes.reverse(i, min(len(data_bytes), i+8))
        if len(data_bytes) % 8 != 0:
            data_bytes.prepend("0b" + "0"*(8-(len(data_bytes) % 8)))
        return data_bytes.bytes

    def bitstream_to_value(self, data_bitstream, offset, length):
        data_bytes = data_bitstream[offset:offset+length]
        data_bytes.reverse()
        if len(data_bytes) % 8 != 0:
            data_bytes.prepend("0b" + "0"*(8-(len(data_bytes) % 8)))
        return int(data_bytes.hex, 16)

    def get_image(self, data, filename, color_table, idx_transparent):
        lSrcScanBytes = (self.width + 3) & 0xfc
        # Each is RGBQUAD (4 bytes: R,G,B,Reserved)
        lTrgScanBytes = self.width * 4
        image_data = np.zeros((self.height,self.width,3), dtype=np.uint8)

        count = 0
        for y in range(self.height):
            lSrcNdx = y * self.width

            for x in range(self.width):
                try:
                    color = color_table[data[lSrcNdx]].color
                except Exception as e:
                    # TODO: why not just exit? why catch exception?
                    continue
                image_data[self.height-1-y,x] = [color.red, color.green, color.blue]
                lSrcNdx += 1

        pic = Image.fromarray(image_data)
        pic.save(filename)

    def decompress_img_in_place(self):
        # Bonz say NO.        