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
    def __init__(self, matrix, type, format, predictor):
        self.original_matrix = matrix
        self.predictor = predictor
        self.type = type if type in ["Y", "U", "V"] else None
        self.format = format    # TODO veririfcar se é array naqules 3 formatos
        self.encoded_matrix = np.empty(self.original_matrix.shape)  # sighly faster
        # Golomb encoder
        self.golomb = Golomb(4)
        self.golomb_codes = self.golomb.load_golomb_codes()
        self.bitstream = BitStream("./predictor.bin", "wb")
    
    def write_code(self, code):
        for bit in code:
            self.bitstream.writeBit(bit,1)

    def encode(self):
        if not self.type:
            logger.error("Matrix Type {} not valid; Must be one of ['Y', 'U', 'V']. Aborting.".format(self.type))
            return False
            
        # TODO: ver o que é aquele K do stor
        if self.format == [4,4,4]:

            # write header with bitstream
            self.bitstream.writeString("{}\t{}".format(self.original_matrix.shape[0],self.original_matrix.shape[1]))

            # matrix size/shape is the same no mather which one

            self.encoded_matrix[0, 0] = self.original_matrix[0,0] - self.predictor.predict(0,0,0)
            self.write_code(self.golomb_codes[self.encoded_matrix[0, 0]])

            for col in range(1, self.original_matrix.shape[1]):
                self.encoded_matrix[0, col] = int(self.original_matrix[0, col]) - self.predictor.predict(self.original_matrix[0, col -1], 0, 0)
                self.write_code(self.golomb_codes[self.encoded_matrix[0, col]])

            for line in range(1, self.original_matrix.shape[0]):
                self.encoded_matrix[line, 0] = int(self.original_matrix[line, 0]) - self.predictor.predict(0, self.original_matrix[line - 1, 0], 0)
                self.write_code(self.golomb_codes[self.encoded_matrix[line, 0]])


            for line in range(1, self.original_matrix.shape[0]):
                for col in range(1, self.original_matrix.shape[1]):
                    # print("line: ", line, ", col: ", col, "; original: ", self.original_matrix[line, col], ", predict: ", self.original_matrix[line, col - 1], self.original_matrix[line - 1, col], self.original_matrix[col - 1, line -1])
                    self.encoded_matrix[line, col] = int(self.original_matrix[line, col]) - self.predictor.predict(
                        self.original_matrix[line, col - 1], self.original_matrix[line - 1, col], self.original_matrix[line - 1, col -1])
                    self.write_code(self.golomb_codes[self.encoded_matrix[line, col]])
            
            

if __name__ == "__main__":
    frame = Frame444(1280, 720, "../media/park_joy_444_720p50.y4m")
    frame.advance()
    matrix2 = frame.getY()
    print(matrix2)
    print("-----")
    # matrix2 = np.zeros([12, 10])
    # matrix2[0,0] = 20
    # matrix2[0,1] = 30
    # matrix2[0,2] = 32
    # matrix2[0,3] = 33
    # matrix2[0,4] = 34
    # matrix2[1,0] = 25
    # matrix2[1,1] = 10
    # matrix2[1,2] = 12
    # matrix2[2,0] = 40
    # print(matrix2)
    print("------")
    ife = IntraFrameEncoder(matrix2, "Y", [4,4,4], Predictors.JPEG1)
    ife.encode()
    print(ife.encoded_matrix)

