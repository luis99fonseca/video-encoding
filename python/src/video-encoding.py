import datetime
import logging
import predictors
from frames import *
from encoders import IntraFrameEncoder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('root')
logger.setLevel(logging.INFO)

c_handler = logging.StreamHandler()
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(logging.Formatter('%(name)s | %(levelname)s ->: %(message)s'))

logger.addHandler(c_handler)
logger.propagate = False  # https://stackoverflow.com/a/19561320


if __name__ == '__main__':

    frame = Frame444(720,1280, "../media/park_joy_444_720p50.y4m")

    total = 0
    while True:
        codes = []
        start = datetime.datetime.now()

        playing = frame.advance()
        if not playing:
            break

        # encode Y matrix
        matrix = frame.getY()
        print("Matrix 'Y': {}".format(matrix))
        ife = IntraFrameEncoder(matrix, predictors.JPEG1)
        ife.encode()
        codes += ife.codes
        print("Encoded Matrix 'Y': {}".format(ife.encoded_matrix))
        
        # encode U matrix
        matrix = frame.getU()
        print("Matrix 'U': {}".format(matrix))
        ife.setMatrix(matrix)
        # ife = IntraFrameEncoder(matrix, predictors.JPEG1) # ife.setMatrix(matrix)
        ife.encode()
        codes += ife.codes
        print("Encoded Matrix 'U': {}".format(ife.encoded_matrix))

        # encode V matrix
        matrix = frame.getV()
        print("Matrix 'V': {}".format(matrix))
        # ife = IntraFrameEncoder(matrix, predictors.JPEG1)   # ife.setMatrix(matrix)
        ife.setMatrix(matrix)
        ife.encode()
        codes += ife.codes
        print("Encoded Matrix 'V': {}".format(ife.encoded_matrix))
        
        end = datetime.datetime.now() - start
        print("Compressed frame in {} s.".format(end.seconds))
        total += end.seconds
        # break # com este break só codifica um frame

        start = datetime.datetime.now()
        ife.bitstream.writeString("\nFRAME")
        for code in codes:
            ife.bitstream.writeBit(code, 1)
        end = datetime.datetime.now() - start
        total += end.seconds
        print("Writed compressed frame in {} s.".format(end.seconds))
        codes = []
