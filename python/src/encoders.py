import numpy as np
import time
import predictors
import logging
from frames import *
from golomb import Golomb
from bitStream import BitStream


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
        self.bitstream = BitStream("../out/encoded_park_joy_444_720p50.bin", "wb")
        self.written_bits = 0 # TODO: tira isto
        self.codes = []

    def write_code(self, code):
        for bit in code:
            self.written_bits += 1
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

            self.encoded_matrix[0, 0] = int(self.original_matrix[0,0] - self.predictor.predict(0,0,0))

            for col in range(1, self.original_matrix.shape[1]):
                self.encoded_matrix[0, col] = int(self.original_matrix[0, col]) - self.predictor.predict(self.original_matrix[0, col -1], 0, 0)

            for line in range(1, self.original_matrix.shape[0]):
                self.encoded_matrix[line, 0] = int(self.original_matrix[line, 0]) - self.predictor.predict(0, self.original_matrix[line - 1, 0], 0)
   
            for line in range(1, self.original_matrix.shape[0]):
                for col in range(1, self.original_matrix.shape[1]):
                    # print("line: ", line, ", col: ", col, "; original: ", self.original_matrix[line, col], ", predict: ", self.original_matrix[line, col - 1], self.original_matrix[line - 1, col], self.original_matrix[col - 1, line -1])
                    self.encoded_matrix[line, col] = int(self.original_matrix[line, col]) - self.predictor.predict(
                        self.original_matrix[line, col - 1], self.original_matrix[line - 1, col], self.original_matrix[line - 1, col -1])
            
            for line in range(self.encoded_matrix.shape[0]):
                for col in range(self.encoded_matrix.shape[1]):
                    #self.write_code(self.golomb.encoded_values[self.encoded_matrix[line, col]])
                    self.codes += self.golomb.encoded_values[self.encoded_matrix[line, col]]
                
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

            for line in range(1, self.original_matrix.shape[0]):
                for col in range(1, self.original_matrix.shape[1]):
                    self.decoded_matrix[line, col] = int(self.original_matrix[line, col]) + self.predictor.predict(
                        self.decoded_matrix[line, col - 1], self.decoded_matrix[line - 1, col],
                        self.decoded_matrix[line - 1, col - 1])
            
        
if __name__ == "__main__":
    frame = Frame444(720,1280, "../media/park_joy_444_720p50.y4m")
    """
    frame.advance()
    matrix = frame.getY()
    ife = IntraFrameEncoder(matrix, "Y", [4,4,4], predictors.JPEG1)
    ife.encode()

    print(ife.encoded_matrix)
    """
    import datetime
    total = 0
    codes = []
    while True:
        start = datetime.datetime.now()
        playing = frame.advance()
        if not playing:
            break

        # encode Y matrix
        matrix = frame.getY()
        print("Matrix 'Y': {}".format(matrix))
        ife = IntraFrameEncoder(matrix, "Y", [4,4,4], predictors.JPEG1)
        ife.encode()
        codes.append(ife.codes)
        print("Encoded Matrix 'Y': {}".format(ife.encoded_matrix))
        
        # encode U matrix
        matrix = frame.getU()
        print("Matrix 'U': {}".format(matrix))
        ife = IntraFrameEncoder(matrix, "U", [4,4,4], predictors.JPEG1)
        ife.encode()
        codes.append(ife.codes)
        print("Encoded Matrix 'U': {}".format(ife.encoded_matrix))

        # encode V matrix
        matrix = frame.getV()
        print("Matrix 'V': {}".format(matrix))
        ife = IntraFrameEncoder(matrix, "V", [4,4,4], predictors.JPEG1)
        ife.encode()
        codes.append(ife.codes)
        print("Encoded Matrix 'V': {}".format(ife.encoded_matrix))
        
        end = datetime.datetime.now() - start
        print("Compressed frame in {} s. Total bits: {}".format(end.seconds, ife.written_bits))
        total += end.seconds
        

    matrixes = ["Y", "U", "V"]
    for code in codes:
        decoded = ife.golomb.stream_decoder(code)
        decoded = np.array(decoded, dtype=np.int16).reshape((720,1280))
        print("Decoded: {}".format(decoded))
        ifd = IntraFrameDecoder(decoded, matrixes.pop(0), [4,4,4], predictors.JPEG1)
        ifd.decode()
        print("Original matrix: {}".format(ifd.decoded_matrix))



    