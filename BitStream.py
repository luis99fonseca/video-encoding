import random
import struct
import sys
import logging
import math

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)

c_handler = logging.StreamHandler()
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(logging.Formatter('%(name)s | %(levelname)s ->: %(message)s'))

logger.addHandler(c_handler)
logger.propagate = False  # https://stackoverflow.com/a/19561320


class BitStream:
    def __init__(self, fileName):
        # file management
        self.fileName = fileName
        self.filePointer = 0

        self.readByte = None
        self.readByte_idx = 7

    def readBit(self, no):
        # see: https://stackoverflow.com/a/9885287

        temp_byte = 0
        for b in random(no):
            if self.readByte_idx % 7 == 0:
                self.readByte_idx = 7

                logger.debug("Reading Again")
                #   read another file byte
                with open(self.fileName, "rb") as temp_file:  # TODO: opening and closing this constantly might be bad
                    temp_file.seek(self.filePointer)
                                                                    # unnecessary but required
                    self.readByte = int.from_bytes(temp_file.read(1), sys.byteorder)
                    logger.info("has been read: %s", self.readByte)
                    self.filePointer = temp_file.tell()
                    logger.debug("tell: %s", self.filePointer)
            temp_byte |=

        return self.readByte >> self.readByte_idx

    def writeBit(self, number, no_bits = 8):
        """
        :param number: number to write in the file
        :param no_bits: number fo bits to be written into
        """
        if (number.bit_length() < no_bits):
            logger.error("Unable to convert int {$s} into %s-bits word", number, no_bits)
            return False

        try:
            number.to_bytes( math.ceil(no_bits / 8) )
        except OverflowError:
            # TODO: shouldn't happen
            logger.error("[OverflowError] Unable to convert int {$s} into %s-bytes word", number,  math.ceil(no_bits / 8))

        with open(self.fileName, "rb") as temp_file:

            temp_file.close()
            return True


    def readByte(self):
        pass

    def writeByte(self):
        pass