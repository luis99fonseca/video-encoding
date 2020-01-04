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

    frame = Frame444(720, 1280, "../media/park_joy_444_720p50.y4m")

    import datetime
    total = 0
    firstFrame = True
    ife = IntraFrameEncoder(predictors.JPEG1)
    for _ in range(2):
        start = datetime.datetime.now()
        playing = frame.advance()

        # movie end
        if not playing:
            break

        # encode Y matrix
        matrix = frame.getY()
        ife.setMatrix(matrix)
        if firstFrame:
            ife.bitstream.writeString("720\t1280")  # hard coded for now
        ife.encode()
        print(ife.encoded_matrix)

        # encode U matrix
        matrix = frame.getU()
        ife.setMatrix(matrix)
        ife.encode()

        # encode V matrix
        matrix = frame.getV()
        ife.setMatrix(matrix)
        ife.encode()

        end = datetime.datetime.now() - start
        print("Frame compressed in {} s. Total bits: {}".format(end.seconds, ife.written_bits))
        total += end.seconds

        firstFrame = False
        # com este break só codifica um frame
        # break
    ife.bitstream.closeFile()
    print("Compressed frames in {} s.".format(total))