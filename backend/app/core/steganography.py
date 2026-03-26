#!/usr/bin/env python
# coding:UTF-8

from typing import Callable, Optional

import numpy as np
from numpy.typing import NDArray

from .cryptography import Cryptography

# Header stores the data length as a 64-bit integer
HEADER_BITS = 64
HEADER_BYTES = HEADER_BITS // 8
BITS_PER_BYTE = 8
MAX_BIT_PLANES = 8


class SteganographyException(Exception):
    pass


class Steganography:
    def __init__(self, im: NDArray, crypto: Cryptography):
        self.image = im
        self.crypto = crypto
        self.height, self.width, self.nbchannels = im.shape
        self.size = self.width * self.height

        self.maskONEValues = [1, 2, 4, 8, 16, 32, 64, 128]
        self.maskONE = self.maskONEValues.pop(0)

        self.maskZEROValues = [254, 253, 251, 247, 239, 223, 191, 127]
        self.maskZERO = self.maskZEROValues.pop(0)

        self.curwidth = 0
        self.curheight = 0
        self.curchan = 0

    def capacity_bytes(self) -> int:
        """Return the maximum number of data bytes that can be hidden in this image."""
        total_bits = self.width * self.height * self.nbchannels * MAX_BIT_PLANES
        return (total_bits // BITS_PER_BYTE) - HEADER_BYTES

    def put_binary_value(self, bits: str) -> None:
        for c in bits:
            val = list(self.image[self.curheight, self.curwidth])
            if int(c) == 1:
                val[self.curchan] = int(val[self.curchan]) | self.maskONE
            else:
                val[self.curchan] = int(val[self.curchan]) & self.maskZERO

            self.image[self.curheight, self.curwidth] = tuple(val)
            self.next_slot()

    def next_slot(self) -> None:
        if self.curchan == self.nbchannels - 1:
            self.curchan = 0
            if self.curwidth == self.width - 1:
                self.curwidth = 0
                if self.curheight == self.height - 1:
                    self.curheight = 0
                    if self.maskONE == 128:
                        raise SteganographyException(
                            "No available slot remaining (image filled)")
                    else:
                        self.maskONE = self.maskONEValues.pop(0)
                        self.maskZERO = self.maskZEROValues.pop(0)
                else:
                    self.curheight += 1
            else:
                self.curwidth += 1
        else:
            self.curchan += 1

    def read_bit(self) -> str:
        val = self.image[self.curheight, self.curwidth][self.curchan]
        val = int(val) & self.maskONE
        self.next_slot()
        return "1" if val > 0 else "0"

    def read_byte(self) -> str:
        return self.read_bits(BITS_PER_BYTE)

    def read_bits(self, nb: int) -> str:
        bits = ""
        for _ in range(nb):
            bits += self.read_bit()
        return bits

    def byteValue(self, val: int) -> str:
        return self.binary_value(val, BITS_PER_BYTE)

    def binary_value(self, val: int, bitsize: int) -> str:
        binval = bin(val)[2:]
        if len(binval) > bitsize:
            raise SteganographyException(
                "binary value larger than the expected size")
        return binval.zfill(bitsize)

    def encode_text(self, text: str) -> NDArray:
        enc_data = self.crypto.encrypt(text)
        return self.encode_binary(enc_data)

    def decode_text(self) -> str:
        enc_text = self.decode_binary()
        return self.crypto.decrypt_text(enc_text)

    def encode_binary(
        self,
        data: bytes,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> NDArray:
        total = len(data)
        if total > self.capacity_bytes():
            raise SteganographyException(
                f"Carrier image not big enough ({self.capacity_bytes()} bytes capacity, "
                f"{total} bytes needed)")

        self.put_binary_value(self.binary_value(total, HEADER_BITS))

        for i, byte in enumerate(data):
            byte = byte if isinstance(byte, int) else ord(byte)
            self.put_binary_value(self.byteValue(byte))
            if progress_callback and (i % 1024 == 0 or i == total - 1):
                progress_callback(i + 1, total)

        return self.image

    def decode_binary(
        self,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> bytes:
        total = int(self.read_bits(HEADER_BITS), 2)
        output = b""

        for i in range(total):
            output += bytearray([int(self.read_byte(), 2)])
            if progress_callback and (i % 1024 == 0 or i == total - 1):
                progress_callback(i + 1, total)

        return output
