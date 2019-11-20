import random
import struct
import sys
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)

c_handler = logging.StreamHandler()
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(logging.Formatter('%(name)s | %(levelname)s ->: %(message)s'))

logger.addHandler(c_handler)
logger.propagate = False    #   https://stackoverflow.com/a/19561320


class BitStream():
    def __init__(self, fileName):

        # file management
        self.fileName = fileName
        self.filePointer = 0  # NOTE: with bitsRead alone we could infer the pointer

        # read control
        self.bitsRead = 0
        self.mask = 128  # aka 10000000
        self.byte = None  # byte actual

    # Note: Not sure if this is what is meant to do, welp... verificar amanha
    def readBit(self, no):
        # if self.bitsRead % 8 == 0:
        #     logger.debug("Reading...")
        #     temp_file = open(self.fileName, "rb")
        #     self.byte = int.from_bytes(temp_file.read(1), sys.byteorder)  # reads a byte
        #     self.filePointer = temp_file.tell()
        #     logger.debug("tell: %s", self.filePointer)
        #     temp_file.close()

        #   quick fix, to not allow reading from another byte
        # logger.error((self.bitsRead % 8) + no)
        logger.error((self.bitsRead % 8) + no)
        # assert 0 < (self.bitsRead % 8) + no <= 8

        temp_byte = 0
        for b in range(no):
            if self.bitsRead % 8 == 0:
                logger.debug("Reading Again")
                #   read another file byte
                temp_file = open(self.fileName, "rb")   # TODO: opening and closing this constantly might be bad
                temp_file.seek(self.filePointer)

                #   manage file pointer
                self.byte = int.from_bytes(temp_file.read(1), sys.byteorder)  # reads a byte
                self.filePointer = temp_file.tell()
                logger.debug("tell: %s", self.filePointer)
                temp_file.close()

            #   work with bit at b'th
            temp_byte |= self.byte & (self.mask >> (self.bitsRead % 8))
            logger.warning("> b:    %s - bits_read: %s, rest: %s", b, self.bitsRead, (self.bitsRead % 8))
            self.bitsRead += 1

        logger.debug("return %s", temp_byte)
        return temp_byte

    def writeBit(self, no):
        #   TODO: ask teacher if we can store the bits until a byte is formed
        pass

    def readbyte(self):
        return self.readBit(8)

    def writeByte(self):
        return self.readBit(8)
#
#
coiso = BitStream("new_town.txt")
coiso.readBit(7)
coiso.readBit(1)
coiso.readBit(7)
coiso.readBit(20)
# TODO: ignore but don't delete
# # with open("old_town.txt", "rb") as file:
# #     linha0 = file.readline()
# #     print("linha 1", linha0.decode().rstrip())
# #     linha1 = file.readline()
# #     print("linha 2", linha1.decode().rstrip())
# #     linha2 = file.read(1)
# #
# #     '''
# #     https://stackoverflow.com/questions/34009653/convert-bytes-to-int
# #     '''
# #     print("linha 3", int.from_bytes(linha2, "big"))
# #     print((linha2))
# #     for l in linha2:
# #         print(">>", l)
# #
# #     while True:
# #         ola = file.read(1)
# #         # print("l ", len(ola))
# #         print("> ", int.from_bytes(ola, "big"))
# #         if not len(ola):
# #             break
#
# with open("new_town.txt", "wb") as nfile:
#     for i in range(2):
#         r = 1 # random.randint(1, 10)
#         nfile.write(struct.pack("<i", r))     #> big-endian / <nothing> or @ native; i integer
#         print("writing: ", r)

with open("new_town.txt", "rb") as nfile:
    while True:
        ola = nfile.read(4)
        if not len(ola):
            break
        print("> ", int.from_bytes(ola, sys.byteorder))
#
#
# # https://stackoverflow.com/questions/10365624/sys-getsizeofint-returns-an-unreasonably-large-value
# print(sys.getsizeof(int()))
