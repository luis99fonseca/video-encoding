import numpy as np
import time
import Predictors
import logging
from Frames import *
from golomb import Golomb
from BitStream import BitStream

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('root')
logger.setLevel(logging.INFO)

c_handler = logging.StreamHandler()
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(logging.Formatter('%(name)s | %(levelname)s ->: %(message)s'))

logger.addHandler(c_handler)
logger.propagate = False  # https://stackoverflow.com/a/19561320


class IntraFrameEncoder():
    """
    Lossless intra-frame encoder
    """

    def __init__(self, matrix, predictor):
        self.original_matrix = matrix
        self.predictor = predictor
        self.encoded_matrix = np.empty(self.original_matrix.shape)  # sighly faster

        # Golomb encoder
        self.golomb = Golomb(4)
        self.bitstream = BitStream("./encoded_park_joy_444_720p50.bin", "wb")

    def write_code(self, code):
        for bit in code:
            self.bitstream.writeBit(bit, 1)

    def setMatrix(self, new_matrix):
        self.original_matrix = new_matrix

    def encode(self):

        # TODO: ver o que é aquele K do stor
        # write header with bitstream
        self.bitstream.writeString("{}\t{}".format(self.original_matrix.shape[0], self.original_matrix.shape[1]))

        self.encoded_matrix[0, 0] = int(self.original_matrix[0, 0] - self.predictor.predict(0, 0, 0))

        for col in range(1, self.original_matrix.shape[1]):
            self.encoded_matrix[0, col] = int(self.original_matrix[0, col]) - self.predictor.predict(
                self.original_matrix[0, col - 1], 0, 0)

        for line in range(1, self.original_matrix.shape[0]):
            self.encoded_matrix[line, 0] = int(self.original_matrix[line, 0]) - self.predictor.predict(0,
                                                                                                       self.original_matrix[
                                                                                                           line - 1, 0],
                                                                                                       0)

        for line in range(1, self.original_matrix.shape[0]):
            for col in range(1, self.original_matrix.shape[1]):
                # print("line: ", line, ", col: ", col, "; original: ", self.original_matrix[line, col], ", predict: ", self.original_matrix[line, col - 1], self.original_matrix[line - 1, col], self.original_matrix[col - 1, line -1])
                self.encoded_matrix[line, col] = int(self.original_matrix[line, col]) - self.predictor.predict(
                    self.original_matrix[line, col - 1], self.original_matrix[line - 1, col],
                    self.original_matrix[line - 1, col - 1])

        for line in range(self.encoded_matrix.shape[0]):
            for col in range(self.encoded_matrix.shape[1]):
                self.write_code(self.golomb.encoded_values[self.encoded_matrix[line, col]])


class IntraFrameDecoder():
    """
    Lossless intra-frame decoder, complementing the one analogous encoder
    """

    def __init__(self, matrix, predictor):
        self.original_matrix = matrix
        self.predictor = predictor
        self.decoded_matrix = np.empty(self.original_matrix.shape)  # sighly faster
        # self.encoded = False
    
    def setMatrix(self, new_matrix):
        self.original_matrix = new_matrix
    
    def decode(self):

        # TODO: ver o que é aquele K do stor
        self.decoded_matrix[0, 0] = self.original_matrix[0, 0] + self.predictor.predict(0, 0, 0)

        for col in range(1, self.original_matrix.shape[1]):
            self.decoded_matrix[0, col] = int(self.original_matrix[0, col]) + self.predictor.predict(
                self.decoded_matrix[0, col - 1], 0, 0)

        for line in range(1, self.original_matrix.shape[0]):
            self.decoded_matrix[line, 0] = int(self.original_matrix[line, 0]) + self.predictor.predict(0,
                                                                                                       self.decoded_matrix[
                                                                                                           line - 1, 0],
                                                                                                       0)

        print("1 ", self.original_matrix.shape[1])
        for line in range(1, self.original_matrix.shape[0]):
            for col in range(1, self.original_matrix.shape[1]):
                # print("line: ", line, ", col: ", col, "; original: ", self.original_matrix[line, col], ", predict: ", self.original_matrix[line, col - 1], self.original_matrix[line - 1, col], self.original_matrix[col - 1, line -1])
                self.decoded_matrix[line, col] = int(self.original_matrix[line, col]) + self.predictor.predict(
                    self.decoded_matrix[line, col - 1], self.decoded_matrix[line - 1, col],
                    self.decoded_matrix[line - 1, col - 1])


if __name__ == "__main__":
    frame = Frame420(720, 1280, "../media/park_joy_420_720p50.y4m")

    frame.advance()
    matrix = frame.getU()
    ife = IntraFrameEncoder(matrix, Predictors.JPEG1)
    ife.encode()

    print(ife.encoded_matrix)
    print(ife.encoded_matrix.shape)

    """
    import datetime
    start = datetime.datetime.now()
    #while True:
    playing = frame.advance()
    if not playing:
        pass # break
    matrix = frame.getY()
    ife = IntraFrameEncoder(matrix, "Y", [4,4,4], Predictors.JPEG1)
    ife.encode()
    matrix = frame.getU()
    ife = IntraFrameEncoder(matrix, "U", [4,4,4], Predictors.JPEG2)
    ife.encode()
    matrix = frame.getV()
    ife = IntraFrameEncoder(matrix, "V", [4,4,4], Predictors.JPEG3)
    ife.encode()
    end = datetime.datetime.now() - start
    print("Compressed in {} s".format(end.seconds))
    """
