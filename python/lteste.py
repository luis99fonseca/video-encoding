import random
import struct
import sys

# with open("new_town.txt", "wb") as f:
#     f.write((200).to_bytes(1,byteorder="big"))
#     f.write((120).to_bytes(1,byteorder="big"))
#     f.write((99).to_bytes(1,byteorder="big"))
#
#     # ou bytes([1])
#
# with open("new_town.txt", "rb") as f:
#     by = f.read(1)
#     print(">>", by)
#     print(">>", int.from_bytes(by, byteorder='little') << 1)
#
#
#
# byte = 0
# byte = 1 << 1
# print("..", bytes([byte]))

try:
    print((256).to_bytes(3, byteorder="big"))
    print((2).bit_length())
except OverflowError as e:
    print("aaa", e)
