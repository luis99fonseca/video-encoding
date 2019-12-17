from BitStream import BitStream
from golomb import Golomb 

import numpy as np

if __name__ == '__main__':
    golomb = Golomb(4)
    a = golomb.load_golomb_codes()
    bitstream = BitStream("./encoded_park_joy_444_720p50.bin", "rb")
    print(bitstream.readString())
    codes = []
    while True:
        bit = bitstream.readBit(1)
        if not bit:
            break 
        codes += bit

    decoded = golomb.stream_decoder(codes)
    decoded = np.array(decoded, dtype=np.int8).reshape((720,1280))
    print(decoded)