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

"""
This program encodes 500 frames from the video "park_joy_444_720p50.y4m".
"""
if __name__ == '__main__':

    frame = Frame444(720, 1280, "../media/park_joy_444_720p50.y4m")

    total = 0
    firstFrame = True
    ife = IntraFrameEncoder(predictors.JPEG1)
    frames_no = 0
    while True:
        start = datetime.datetime.now()
        playing = frame.advance()

        # movie end
        if not playing:
            break

        # encode Y matrix
        matrix = frame.getY()
        ife.setMatrix(matrix)
        if firstFrame:
            firstFrame = False
            ife.bitstream.writeString("F500\tH720\tW1280\tC444\tS50")  # has to be concordant with Frame initialization above
        ife.encode()

        # encode U matrix
        matrix = frame.getU()
        ife.setMatrix(matrix)
        ife.encode()

        # encode V matrix
        matrix = frame.getV()
        ife.setMatrix(matrix)
        ife.encode()

        end = datetime.datetime.now() - start
        total += end.seconds
        frames_no += 1
        print("Frame compressed in {} s. Total bits: {}. Frames no. {}".format(end.seconds, ife.written_bits, frames_no))
        
        # com este break só codifica um frame
        if frames_no == 3:
        	break
        
    ife.bitstream.closeFile()
    print("Compressed frames in {} s.".format(total))