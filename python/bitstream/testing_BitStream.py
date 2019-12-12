from BitStream import BitStream
import logging

test01 = False
test02 = False
test03 = True

logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)

# ---------------READING TESTING--------------
if test01:
    bitstream01 = BitStream("unitary_tests_out/test01.txt")

    # TODO: verificar se da pa mais de 8
    assert bitstream01.readBit(8) == [1, 1, 0, 0, 1, 0, 0, 0]
    assert bitstream01.readBit(4) == [0, 1, 1, 1]
    assert bitstream01.readBit(4) == [1, 0, 0, 0]
    assert bitstream01.readByte() == [0, 1, 1, 0, 0, 0, 1, 1]
    assert bitstream01.readBit(8) == []
    assert bitstream01.readBit(4) == []

# ---------------WRITING TESTING--------------

if test02:
    bitstream02 = BitStream("unitary_tests_out/test02.txt")

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

    bitstream02 = BitStream("unitary_tests_out/test02.txt")
    assert bitstream02.readBit(8) == [1, 1, 0, 1, 0, 1, 0, 0]
    assert bitstream02.readBit(8) == [0, 0, 0, 0, 0, 0, 0, 1]
    assert bitstream02.readBit(8) == [1, 0, 0, 1, 0, 0, 0, 1]

    assert bitstream02.readBit(8) == [0, 0, 0, 0, 0, 0, 0, 0]
    assert bitstream02.readBit(8) == [0, 0, 0, 0, 0, 0, 1, 1]


if test03:
    bitstream03 = BitStream("unitary_tests_out/test03.txt")

    bitstream03.writeBit(1, 7)
    bitstream03.writeBit(3, 2)

    print(bitstream03.readBit(10))

    pass