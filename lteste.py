import random
import struct
import sys


buffer = 0
filePointer = 0



f = open("new_town.txt", "rb")
# temp_byte = 0
bitsRead2 = 0
mask = 128 # aka 10000000


readingBits = 1
thatByte = f.read(readingBits)

print("adeus", thatByte)
byte = int.from_bytes(thatByte, sys.byteorder) & 255
print("ola", byte)

def getBits(no, bitsRead):
    temp_byte = 0
    print(">>", byte)
    for i in range(no):
        temp_byte |= byte & (mask >> bitsRead)
        bitsRead += 1
    print("return", temp_byte)

getBits(9, bitsRead2)
print("bit.", bitsRead2)

print(f.read(readingBits))
print(f.read(readingBits))
print(f.read(readingBits))
print(f.read(readingBits))

f.close()
