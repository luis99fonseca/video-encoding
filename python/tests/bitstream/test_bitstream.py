from bitStream import BitStream
import logging

test01 = True
test02 = True
test03 = True
test04 = True
test05 = True
test06 = True

logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)

# ---------------READING TESTING--------------
if test01:
    bitstream01 = BitStream("./out/test01.txt", "rb")

    assert bitstream01.readBit(8) == [1, 1, 0, 0, 1, 0, 0, 0]
    assert bitstream01.readBit(4) == [0, 1, 1, 1]
    assert bitstream01.readBit(4) == [1, 0, 0, 0]
    assert bitstream01.readByte() == [0, 1, 1, 0, 0, 0, 1, 1]
    assert bitstream01.readBit(8) == []
    assert bitstream01.readBit(4) == []

    bitstream01.closeFile()

# ---------------WRITING TESTING--------------

if test02:
    bitstream02 = BitStream("./out/test02.txt", "wb")

    assert not bitstream02.writeBit(256, 1)
    assert not bitstream02.writeBit(3, 1)

    bitstream02.writeBit(3, 2)
    bitstream02.writeBit(1, 2)
    bitstream02.writeBit(4, 4)
    bitstream02.writeByte(1)
    bitstream02.writeBit(1, 1)
    bitstream02.writeBit(1, 3)
    bitstream02.writeBit(1, 4)

    bitstream02.writeBit(1, 15)
    bitstream02.writeBit(1, 1)

    bitstream02.writeBit(1, 1)
    bitstream02.writeBit(2, 3)

    assert not bitstream02.readBit(4)

    bitstream02.closeFile()

    bitstream02 = BitStream("./out/test02.txt", "rb")
    assert bitstream02.readBit(8) == [1, 1, 0, 1, 0, 1, 0, 0]
    assert bitstream02.readBit(8) == [0, 0, 0, 0, 0, 0, 0, 1]
    assert bitstream02.readBit(8) == [1, 0, 0, 1, 0, 0, 0, 1]

    assert bitstream02.readBit(8) == [0, 0, 0, 0, 0, 0, 0, 0]
    assert bitstream02.readBit(8) == [0, 0, 0, 0, 0, 0, 1, 1]
    assert bitstream02.readBit(8) == [1, 0, 1, 0, 0, 0, 0, 0]

    assert not bitstream02.writeBit(1,2)


    bitstream02.closeFile()

# ---------------STRING TESTING--------------
if test03:

    bitstream03 = BitStream("./out/test03.txt", "wb")

    bitstream03.writeString("ola")
    bitstream03.writeString("adeus")
    bitstream03.closeFile()

    bitstream03 = BitStream("./out/test03.txt", "rb")

    assert (bitstream03.readString()) == "ola\n"
    assert (bitstream03.readString()) == "adeus\n"
    print(bitstream03.readString(), end="")

    bitstream03.closeFile()

# ---------------WRITING TESTING--------------
if test04:

    bitstream04 = BitStream("./out/test04.txt", "wb")

    t_array01 = [1,0,1,1,1,1,0,1,0,1,1]
    bitstream04.writeArray(t_array01)

    bitstream04.closeFile()

    bitstream04 = BitStream("./out/test04.txt", "rb")

    assert bitstream04.readBit(len(t_array01)) == t_array01

    bitstream04.closeFile()

# ---------------INCOMPLETE WRITING/READING TESTING--------------
if test05:
    bitstream05 = BitStream("./out/test05.txt", "wb")

    t_array01 = [1, 0, 1]
    bitstream05.writeArray(t_array01)

    bitstream05.closeFile()

    bitstream05 = BitStream("./out/test05.txt", "rb")

    assert bitstream05.readBit(5) == t_array01 + [0, 0]
    bitstream05.readBit(3)
    bitstream05.readBit(1)
    bitstream05.readBit(1)
    bitstream05.closeFile()

    # -------------------------------
    print("----------------")
    bitstream05 = BitStream("./out/test05.txt", "wb")

    t_array01 = [1,1,1,1,1,1,1]
    bitstream05.writeArray(t_array01)

    bitstream05.closeFile()

    bitstream05 = BitStream("./out/test05.txt", "rb")

    assert bitstream05.readBit(7) == t_array01
    bitstream05.readBit(1)
    bitstream05.readBit(1)
    bitstream05.readBit(1)
    bitstream05.closeFile()

# ---------------ADD NUMBER FEATURE (TO GET MORE EFFICIENCY)--------------
if test06:
    bitstream06 = BitStream("./out/test06.txt", "wbs")

    t_array01 = [1, 1, 1, 1, 1, 1, 1, 1]
    t_array02 = [0, 0, 0, 0, 0, 0, 0, 0]
    t_array03 = [1, 1, 1, 1]
    t_array04 = [1, 1, 1, 1]
    t_array05 = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    t_array06 = [0, 0, 0, 0, 0, 0, 0]

    bitstream06.addNumber(t_array01)
    bitstream06.addNumber(t_array02)
    bitstream06.addNumber(t_array03)
    bitstream06.addNumber(t_array04)
    bitstream06.addNumber(t_array05)
    bitstream06.addNumber(t_array06)

    print(bitstream06.write_array_final)

    bitstream06.closeFile()

    bitstream06 = BitStream("./out/test06.txt", "rb")

    assert bitstream06.readBit(8) == [1, 1, 1, 1, 1, 1, 1, 1]
    assert bitstream06.readBit(8) == [0, 0, 0, 0, 0, 0, 0, 0]
    assert bitstream06.readBit(8) == [1, 1, 1, 1, 1, 1, 1, 1]
    assert bitstream06.readBit(8) == [1, 1, 1, 1, 1, 1, 1, 1]
    assert bitstream06.readBit(8) == [1, 0, 0, 0, 0, 0, 0, 0]




