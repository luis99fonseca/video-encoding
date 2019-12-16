import random
import struct
import sys
import logging
import math

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('root')
logger.setLevel(logging.INFO)

c_handler = logging.StreamHandler()
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(logging.Formatter('%(name)s | %(levelname)s ->: %(message)s'))

logger.addHandler(c_handler)
logger.propagate = False  # https://stackoverflow.com/a/19561320


class BitStream:
    def __init__(self, fileName, mode):
        # file management
        assert mode in ["wb", "rb"]
        self.mode = mode
        self.file = open(fileName, self.mode)

        self.read_byte = None   # buffer
        self.read_byte_idx = -1
        self.read_eof = False

        self.write_byte = 0  # buffer
        self.write_byte_idx = 7
        self.write_mode = "wb"

        self.closed = False

    def closeFile(self):
        if self.read_byte_idx != 7 and self.mode == "wb":
            logger.warning("Writing: %s", bin(self.write_byte))
            self.file.write(self.write_byte.to_bytes(1, byteorder="big"))
        self.file.close()

    def readBit(self, no):
        # see: https://stackoverflow.com/a/9885287
        bit_list = []
        if self.closed:
            logger.error("Class closed! Can't operate any further!")
            return False
        elif self.mode == "wb":
            logger.error("Class defined of Writing only. Not allowed to Read!")
            return False

        elif self.read_eof:
            logger.debug("EOF reached!!! Cannot read any further.")
            return bit_list

        for b in range(no):
            temp_bit = 0
            if self.read_byte_idx == -1:
                self.read_byte_idx = 7

                logger.debug("Reading Again")

                #   read another file byte
                temp_byte = self.file.read(1)
                if not temp_byte:
                    self.read_eof = True
                    logger.debug("EOF reached!! Cannot read any further.")
                    self.closeFile()
                    return bit_list
                else:                                           # irrelevant but required
                    self.read_byte = int.from_bytes(temp_byte, sys.byteorder)
                    logger.debug("has been read: %s, aka %s", self.read_byte, bin(self.read_byte))
                    
            logger.debug("read idx: %s; byte: %s", self.read_byte_idx, self.read_byte)
            temp_bit |= (self.read_byte >> self.read_byte_idx) & 1
            self.read_byte_idx -= 1
            bit_list.append(temp_bit)

        return bit_list

    def writeBit(self, number, no_bits = 8):
        """
        :param number: number to write in the file
        :param no_bits: number fo bits to be written into
        """
        if self.closed:
            logger.error("Class closed! Can't operate any further!")
            return False

        elif self.mode == "rb":
            logger.error("Class defined of Reading only. Not allowed to Write!")
            return False

        elif (number.bit_length() > no_bits):
            logger.error("Unable to convert int {%s} into %s-bits word", number, no_bits)
            return False

        for idx in range(no_bits - 1, -1, -1):
            temp_bit = (number >> idx) & 1  # TODO: tentar simplificar os shifts, so para 1
            logger.debug("idx: %s; temp_bit: %s, write_idx: %s; withShitft: %s; temp2: NONE", idx, temp_bit, self.write_byte_idx, (temp_bit << self.write_byte_idx))
            self.write_byte |= (temp_bit << self.write_byte_idx)
            self.write_byte_idx -= 1

            if self.write_byte_idx == -1:
                logger.warning("Writing: %s", bin(self.write_byte))
                self.file.write(self.write_byte.to_bytes(1, byteorder="big"))
                self.write_mode = "ab"
                self.write_byte_idx = 7
                self.write_byte = 0

        return True

    # @obsolete
    ## doesnt allow to split bytes aka, part of a writing in one byte and another part in the next
    def writeBit2(self, number, no_bits = 8):
        """
        :param number: number to write in the file
        :param no_bits: number fo bits to be written into
        """

        if (number.bit_length() > no_bits):
            logger.error("Unable to convert int {%s} into %s-bits word", number, no_bits)
            return False

        temp_counter = no_bits
        while True:
            if self.write_byte_idx == -1:
                with open(self.fileName, self.write_mode) as temp_file:
                    logger.warning("Writing: %s", bin(self.write_byte))
                    temp_file.write(self.write_byte.to_bytes(1, byteorder="big"))
                    self.write_mode = "ab"
                self.write_byte_idx = 7
                self.write_byte = 0
            if temp_counter <= 0:
                return True
            self.write_byte_idx -= (no_bits % (8 + 1))  # subtracting from the idx the number of "available" bits / we can only write at max 8 bits at the time
            temp_counter -= (no_bits % (8 + 1))
            logger.debug("left: %s ; used: %s", self.write_byte_idx + 1,8 - self.write_byte_idx - 1)
            self.write_byte |= number << self.write_byte_idx + 1    # +1, because there are 8 bits in total, but the starting number is 7, so we adjust it
            logger.debug("i: %s - %s - %s", self.write_byte_idx, bin(self.write_byte), temp_counter)

    def writeString(self, message):
        try:
            self.file.write((message + "\n").encode("utf-8"))
            return True
        except Exception as e:
            logger.error("Could not write to file: ", e)
            return True

    def readString(self):
        """
        Reads and returns an entire line decoded in utf-8 format
        """
        return self.file.readline().decode("utf-8")

    def readByte(self):
        return self.readBit(8)

    def writeByte(self, number):
        return self.writeBit(number, 8)