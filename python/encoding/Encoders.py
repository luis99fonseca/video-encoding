import numpy as np
import time
import Predictors
import logging
from Frames import *

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)

c_handler = logging.StreamHandler()
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(logging.Formatter('%(name)s | %(levelname)s ->: %(message)s'))

logger.addHandler(c_handler)
logger.propagate = False  # https://stackoverflow.com/a/19561320

class IntraFrameEncoder():
    """
    Lossless intra-frame encoder
    """
    def __init__(self, matrix, type, format, predictor):
        self.original_matrix = matrix
        self.predictor = predictor
        self.type = type if type in ["Y", "U", "V"] else None
        self.format = format    # TODO veririfcar se é array naqules 3 formatos
        self.encoded_matrix = np.empty(self.original_matrix.shape)  # sighly faster
        # self.encoded = False

    def encode(self):
        if not self.type:
            logger.error("Matrix Type {} not valid; Must be one of ['Y', 'U', 'V']. Aborting.".format(self.type))
            return False

        # TODO: ver o que é aquele K do stor
        if self.format == [4,4,4]:
            # matrix size/shape is the same no mather which one

            self.encoded_matrix[0, 0] = self.original_matrix[0,0] - self.predictor.predict(0,0,0)

            for col in range(1, self.original_matrix.shape[1]):
                self.encoded_matrix[0, col] = int(self.original_matrix[0, col]) - self.predictor.predict(self.original_matrix[0, col -1], 0, 0)

            for line in range(1, self.original_matrix.shape[0]):
                self.encoded_matrix[line, 0] = int(self.original_matrix[line, 0]) - self.predictor.predict(0, self.original_matrix[line - 1, 0], 0)

            print("1 ", self.original_matrix.shape[1])
            for line in range(1, self.original_matrix.shape[0]):
                for col in range(1, self.original_matrix.shape[1]):
                    # print("line: ", line, ", col: ", col, "; original: ", self.original_matrix[line, col], ", predict: ", self.original_matrix[line, col - 1], self.original_matrix[line - 1, col], self.original_matrix[col - 1, line -1])
                    self.encoded_matrix[line, col] = int(self.original_matrix[line, col]) - self.predictor.predict(
                        self.original_matrix[line, col - 1], self.original_matrix[line - 1, col], self.original_matrix[line - 1, col -1])


class IntraFrameDecoder():
    """
    Lossless intra-frame decoder, complementing the one analogous encoder
    """

    def __init__(self, matrix, type, format, predictor):
        self.original_matrix = matrix
        self.predictor = predictor
        self.type = type if type in ["Y", "U", "V"] else None
        self.format = format  # TODO veririfcar se é array naqules 3 formatos
        self.decoded_matrix = np.empty(self.original_matrix.shape)  # sighly faster
        # self.encoded = False

    def decode(self):
        if not self.type:
            logger.error("Matrix Type {} not valid; Must be one of ['Y', 'U', 'V']. Aborting.".format(self.type))
            return False

        # TODO: ver o que é aquele K do stor
        if self.format == [4, 4, 4]:
            # matrix size/shape is the same no mather which one

            self.decoded_matrix[0, 0] = self.original_matrix[0, 0] + self.predictor.predict(0, 0, 0)

            for col in range(1, self.original_matrix.shape[1]):
                self.decoded_matrix[0, col] = int(self.original_matrix[0, col]) + self.predictor.predict(
                    self.decoded_matrix[0, col - 1], 0, 0)

            for line in range(1, self.original_matrix.shape[0]):
                self.decoded_matrix[line, 0] = int(self.original_matrix[line, 0]) + self.predictor.predict(0,
                                                                                self.decoded_matrix[line - 1, 0],0)

            print("1 ", self.original_matrix.shape[1])
            for line in range(1, self.original_matrix.shape[0]):
                for col in range(1, self.original_matrix.shape[1]):
                    # print("line: ", line, ", col: ", col, "; original: ", self.original_matrix[line, col], ", predict: ", self.original_matrix[line, col - 1], self.original_matrix[line - 1, col], self.original_matrix[col - 1, line -1])
                    self.decoded_matrix[line, col] = int(self.original_matrix[line, col]) + self.predictor.predict(
                        self.decoded_matrix[line, col - 1], self.decoded_matrix[line - 1, col],
                        self.decoded_matrix[line - 1, col - 1])


if __name__ == "__main__":
    frame = Frame444(720, 1280, "../media/park_joy_444_720p50.y4m")
    frame.advance()
    matrix2 = frame.getY()
    print(matrix2)
    print("-----")
    print("------")
    ife = IntraFrameEncoder(matrix2, "Y", [4,4,4], Predictors.JPEG4)
    ife.encode()
    print(ife.encoded_matrix)
    print(ife.encoded_matrix.shape)

    ifd = IntraFrameDecoder(ife.encoded_matrix, "Y", [4,4,4], Predictors.JPEG4)
    ifd.decode()
    print(ifd.decoded_matrix)
