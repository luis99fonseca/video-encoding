import numpy as np
import time
import predictors
import logging
from frames import *
from golomb import Golomb
from bitStream import BitStream
import cv2
import sys
import threading


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
    This class implements a lossless intra-frame encoder, using 7PEG linear predictors.
    """
    def __init__(self, predictor):
        """
        Default constructor.

        @param matrix: initial matrix
        @param predictor: linear predictor
        """
        self.original_matrix = None
        self.predictor = predictor
        self.encoded_matrix = None

        # Golomb encoder
        self.golomb = Golomb(4)
        self.bitstream = BitStream("../out/encoded_park_joy_444_720p50.bin", "wbs")
        self.written_bits = 0 # TODO: tira isto
        self.codes = []

    def write_code(self, code):
        """
        This method writes a list of bits on file, using the Bitstream class.

        @param code: list with bits to encode.
        """
        # for bit in code:
        #     self.written_bits += 1
        #     self.bitstream.writeBit(bit,1)

        self.written_bits += len(code)
        # self.bitstream.writeArray(code)
        self.bitstream.addNumber(code)


    def setMatrix(self, new_matrix):
        """
        This method sets current matrix of the encoder to 'new_matrix'.

        @param new_matrix: new matrix of type Y,U or V.
        """
        self.original_matrix = new_matrix
        if self.encoded_matrix is None:
            self.encoded_matrix = np.empty(self.original_matrix.shape)  # sighly faster
        self.codes = []
    
    def encode(self):
        """
        This method encodes the original matrix in a new one, based on the current predictor.
        It also uses golomb codification for the entropy encoding.
        """
        if self.original_matrix is None:
            logger.error("No matrix to encode was given!")
            return False

        # TODO: ver o que é aquele K do stor
        # write header with bitstream
        #self.bitstream.writeString("{}\t{}".format(self.original_matrix.shape[0],self.original_matrix.shape[1]))

        # matrix size/shape is the same no mather which one
        self.encoded_matrix[0, 0] = int(self.original_matrix[0,0] - self.predictor.predict(0,0,0))

        for col in range(1, self.original_matrix.shape[1]):
            self.encoded_matrix[0, col] = int(self.original_matrix[0, col]) - self.predictor.predict(self.original_matrix[0, col -1], 0, 0)

        for line in range(1, self.original_matrix.shape[0]):
            self.encoded_matrix[line, 0] = int(self.original_matrix[line, 0]) - self.predictor.predict(0, self.original_matrix[line - 1, 0], 0)

        for line in range(1, self.original_matrix.shape[0]):
            for col in range(1, self.original_matrix.shape[1]):
               self.encoded_matrix[line, col] = int(self.original_matrix[line, col]) - self.predictor.predict(
                    self.original_matrix[line, col - 1], self.original_matrix[line - 1, col], self.original_matrix[line - 1, col -1])

        for line in range(self.encoded_matrix.shape[0]):
            for col in range(self.encoded_matrix.shape[1]):
                self.write_code(self.golomb.encoded_values[self.encoded_matrix[line, col]])


class IntraFrameDecoder():
    """
    This class implements a lossless intra-frame decoder, using 7PEG linear predictors.
    """
    def __init__(self, matrix, predictor):
        """
        Default constructor.

        @param matrix: initial matrix
        @param predictor: linear predictor
        """
        self.original_matrix = matrix
        self.predictor = predictor
        self.decoded_matrix = np.empty(self.original_matrix.shape)  # sighly faster

    def setMatrix(self, new_matrix):
        """
        This method sets current matrix of the encoder to 'new_matrix'.

        @param new_matrix: new matrix of type Y,U or V.
        """
        self.original_matrix = new_matrix

    def decode(self):
        """
        This method decodes a predicted matrix in the original one, based on the current predictor.
        """

        # matrix size/shape is the same no mather which one
        self.decoded_matrix[0, 0] = self.original_matrix[0, 0] + self.predictor.predict(0, 0, 0)

        for col in range(1, self.original_matrix.shape[1]):
            self.decoded_matrix[0, col] = int(self.original_matrix[0, col]) + self.predictor.predict(
                self.decoded_matrix[0, col - 1], 0, 0)

        for line in range(1, self.original_matrix.shape[0]):
            self.decoded_matrix[line, 0] = int(self.original_matrix[line, 0]) + self.predictor.predict(0,
                                                                            self.decoded_matrix[line - 1, 0],0)

        for line in range(1, self.original_matrix.shape[0]):
            for col in range(1, self.original_matrix.shape[1]):
                self.decoded_matrix[line, col] = int(self.original_matrix[line, col]) + self.predictor.predict(
                    self.decoded_matrix[line, col - 1], self.decoded_matrix[line - 1, col],
                    self.decoded_matrix[line - 1, col - 1])
