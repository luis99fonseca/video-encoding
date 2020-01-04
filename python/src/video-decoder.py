import numpy as np
import datetime
import logging
import predictors
from bitStream import BitStream
from golomb import Golomb
from frames import *
from encoders import IntraFrameDecoder

if __name__ == '__main__':

    bitstream = BitStream("../out/encoded_park_joy_444_720p50.bin", "rb")
    golomb = Golomb(4)

    # read header
    height, width = bitstream.readString().split("\t")
    height, width = int(height), int(width)

    matrixes = 0
    frames = 0
    decoded_matrixes = []
    stream = []
    while True:

        stream += bitstream.readBit(height*width*8)
        decoded, i = golomb.stream_decoder(stream, height*width)
        stream = stream[i:]
        matrixes += 1

        if len(decoded) < height*width:
            decoded.append(-3)

        decoded = np.array(decoded, dtype=np.int16).reshape((height,width))
        intraFrameDecoder = IntraFrameDecoder(decoded, predictors.JPEG1)
        intraFrameDecoder.decode()
        print(intraFrameDecoder.decoded_matrix)
        decoded_matrixes.append(intraFrameDecoder.decoded_matrix)

        if matrixes % 3 == 0:
            frames += 1
            print("New frame")
        
        if i == 0: # EOF
            break

    print("Video decoded with sucess!")