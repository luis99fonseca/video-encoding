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
    """
    Class optimised to read/write bits from/to a file
    """
    def __init__(self, fileName, mode):
        # file management
        assert mode in ["wb", "rb"]
        self.mode = mode
        self.file = open(fileName, self.mode)

        self.read_byte = None  # buffer
        self.read_byte_idx = -1
        self.read_eof = False

        self.write_byte = 0  # buffer
        self.write_byte_idx = 7

        self.closed = False

    def closeFile(self):
        """
        Closes the file, such that no further operations can be done.
        If there is a incomplete byte to be written, writes it
        """
        if self.write_byte_idx != 7 and self.mode == "wb":
            # logger.warning("Writing: %s", bin(self.write_byte))
            self.file.write(self.write_byte.to_bytes(1, byteorder="big"))
        self.file.close()

    def readBit(self, no):
        """
        @param no: number of bits to read
        @return: list of bits read
        """
        # see: https://stackoverflow.com/a/9885287
        bit_list = []

        if self.mode == "wb":
            logger.error("Class defined of Writing only. Not allowed to Read!")
            return False

        elif self.read_eof:
            logger.debug("EOF reached!!! Cannot read any further.")
            return bit_list

        elif self.closed:
            logger.error("Class closed! Can't operate any further!")
            return False

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
                    self.closed = True
                    self.closeFile()
                    return bit_list
                else:  # irrelevant but required
                    self.read_byte = int.from_bytes(temp_byte, sys.byteorder)
                    logger.debug("has been read: %s, aka %s", self.read_byte, bin(self.read_byte))

            logger.debug("read idx: %s; byte: %s", self.read_byte_idx, self.read_byte)
            temp_bit |= (self.read_byte >> self.read_byte_idx) & 1
            self.read_byte_idx -= 1
            bit_list.append(temp_bit)
        print("retorning: ", bit_list)
        return bit_list

    def writeBit(self, number, no_bits=8):
        """
        :@param number: number to write in the file
        :@param no_bits: number fo bits to be written into
        """

        if self.mode == "rb":
            logger.error("Class defined of Reading only. Not allowed to Write!")
            return False

        elif (number.bit_length() > no_bits):
            logger.error("Unable to convert int {%s} into %s-bits word", number, no_bits)
            return False

        elif self.closed:
            logger.error("Class closed! Can't operate any further!")
            return False

        for idx in range(no_bits - 1, -1, -1):
            temp_bit = (number >> idx) & 1
            logger.debug("idx: %s; temp_bit: %s, write_idx: %s; withShitft: %s; temp2: NONE", idx, temp_bit,
                         self.write_byte_idx, (temp_bit << self.write_byte_idx))
            self.write_byte |= (temp_bit << self.write_byte_idx)
            self.write_byte_idx -= 1

            if self.write_byte_idx == -1:
                # logger.warning("Writing: %s", bin(self.write_byte))
                self.file.write(self.write_byte.to_bytes(1, byteorder="big"))
                self.write_byte_idx = 7
                self.write_byte = 0

        return True

    def writeArray(self, array):
        """
                :@param array: array of numbers to write in the file
                :@param no_bits: number fo bits to be written into
                :@return
        """
        no_bits = 1
        if self.closed:
            logger.error("Class closed! Can't operate any further!")
            return False

        elif self.mode == "rb":
            logger.error("Class defined of Reading only. Not allowed to Write!")
            return False

        for number in array:
            if number.bit_length() > no_bits:
                logger.error("Unable to convert int {%s} into %s-bits word; at array writing", number, no_bits)
                return False

            for idx in range(no_bits - 1, -1, -1):
                temp_bit = (number >> idx) & 1
                logger.debug("idx: %s; temp_bit: %s, write_idx: %s; withShitft: %s; temp2: NONE", idx, temp_bit,
                             self.write_byte_idx, (temp_bit << self.write_byte_idx))
                self.write_byte |= (temp_bit << self.write_byte_idx)
                self.write_byte_idx -= 1

                if self.write_byte_idx == -1:
                    # logger.warning("Writing: %s", bin(self.write_byte))
                    self.file.write(self.write_byte.to_bytes(1, byteorder="big"))
                    self.write_byte_idx = 7
                    self.write_byte = 0

        return True

    def writeString(self, message):
        """
        Writes an entire line decoded in utf-8 format; Line breaker is appended
        :@param message: String to write
        :@return Whether or not the writing was successful
        """
        try:
            self.file.write((message + "\n").encode("utf-8"))
            return True
        except Exception as e:
            logger.error("Could not write to file: ", e)
            return False

    def readString(self):
        """
        Reads and returns an entire line decoded in utf-8 format
        """
        return self.file.readline().decode("utf-8")

    def readByte(self):
        return self.readBit(8)

    def writeByte(self, number):
        return self.writeBit(number, 8)
