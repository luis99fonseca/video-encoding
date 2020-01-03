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
    print(bitstream.readString())
    print(golomb.stream_decoder(bitstream.readBit(500)))

    


    """
    decoded_matrixes = []
    for code in codes:
        # print("code: ", code)
        decoded = ife.golomb.stream_decoder(code)
        decoded = np.array(decoded, dtype=np.int16).reshape((720,1280))
        print("Decoded: {}".format(decoded))
        ifd = IntraFrameDecoder(decoded, predictors.JPEG1)
        ifd.decode()
        decoded_matrixes.append(ifd.decoded_matrix) # UTILIZA ESTA LISTA COM AS MATRIZES PARA DAR DISPLAY
        print("Original matrix: {}".format(ifd.decoded_matrix))
    """