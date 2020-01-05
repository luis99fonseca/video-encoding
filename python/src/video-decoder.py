import numpy as np
import datetime
import logging
import predictors
from bitStream import BitStream
from golomb import Golomb
from frames import *
from encoders import IntraFrameDecoder

"""
This program decodes a 3 frames video. 
"""
if __name__ == '__main__':

    bitstream = BitStream("../out/3_frames_encoded_park_joy_444_720p50.bin", "rb")
    golomb = Golomb(4)

    # read header
    no_frames, height, width = bitstream.readString().split("\t")
    print(no_frames, height, width)
    no_frames, height, width = int(no_frames[1:]), int(height[1:]), int(width[1:])
    
    matrixes = 0
    frames = 0
    decoded_matrixes = []
    stream = []
    total_time = 0
    start = datetime.datetime.now()
    while frames < no_frames:

        stream += bitstream.readBit(height*width*8)
        decoded, i = golomb.stream_decoder(stream, height*width)
        stream = stream[i:]
        matrixes += 1

        decoded = np.array(decoded, dtype=np.int16).reshape((height,width))
        intraFrameDecoder = IntraFrameDecoder(decoded, predictors.JPEG1)
        intraFrameDecoder.decode()
        decoded_matrixes.append(intraFrameDecoder.decoded_matrix)

        if matrixes % 3 == 0:
            end = datetime.datetime.now() - start
            frames += 1
            total_time += end.seconds
            print("Frame decompressed in {} s. Frames no. {}".format(end.seconds, frames))
            start = datetime.datetime.now()
        
        if i == 0: # EOF
            break

    print("Video decoded with sucess!")