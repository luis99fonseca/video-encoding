import numpy as np
import time
import predictors
import logging
from frames import *
from golomb import Golomb
from bitStream import BitStream
import cv2


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
        break # com este break só codifica um frame
        

    matrixes = ["Y", "U", "V"]
    decoded_matrixes = []
    for code in codes:
        decoded = ife.golomb.stream_decoder(code)
        decoded = np.array(decoded, dtype=np.int16).reshape((720,1280))
        print("Decoded: {}".format(decoded))
        ifd = IntraFrameDecoder(decoded, matrixes.pop(0), [4,4,4], predictors.JPEG1)
        ifd.decode()
        decoded_matrixes.append(ifd.decoded_matrix) # UTILIZA ESTA LISTA COM AS MATRIZES PARA DAR DISPLAY
        print("Original matrix: {}".format(ifd.decoded_matrix))

    Y = decoded_matrixes[0]
    U = decoded_matrixes[1]
    V = decoded_matrixes[2]
    YUV = np.dstack((Y, U, V))[:720, :1280, :].astype(np.float)
    YUV[:, :, 0] = YUV[:, :, 0] - 16  # Offset Y by 16
    YUV[:, :, 1:] = YUV[:, :, 1:] - 128  # Offset UV by 128
    # YUV conversion matrix from ITU-R BT.601 version (SDTV)
    # Note the swapped R and B planes!
    #              Y       U       V
    # https://en.wikipedia.org/wiki/YUV#Conversion_to/from_RGB
    M = np.array([[1.164, 2.017, 0.000],  # B
                  [1.164, -0.392, -0.813],  # G
                  [1.164, 0.000, 1.596]])  # R
    # Take the dot product with the matrix to produce BGR output, clamp the
    # results to byte range and convert to bytes
    BGR = YUV.dot(M.T).clip(0, 255).astype(np.uint8)
    # Display the image with OpenCV
    cv2.imshow('image', BGR)
    cv2.waitKey(  # TODO: por waitKey time dinamico: aka ir buscar os FPS
        10000)  # I found that it works if i press the key whilst the window is in focus. If the command line is
    # in focus then nothing happens;
    # Its in milliseconds

    # print("--------------bem-------------")
    # frame = Frame444(720, 1280, "../media/park_joy_444_720p50.y4m")
    # frame.advance()
    # Y = frame.getY()
    # U = frame.getU()
    # V = frame.getV()
    #
    # YUV = np.dstack((Y, U, V))[:720, :1280, :].astype(np.float)
    # YUV[:, :, 0] = YUV[:, :, 0] - 16  # Offset Y by 16
    # YUV[:, :, 1:] = YUV[:, :, 1:] - 128  # Offset UV by 128
    # # YUV conversion matrix from ITU-R BT.601 version (SDTV)
    # # Note the swapped R and B planes!
    # #              Y       U       V
    # # https://en.wikipedia.org/wiki/YUV#Conversion_to/from_RGB
    # M = np.array([[1.164, 2.017, 0.000],  # B
    #               [1.164, -0.392, -0.813],  # G
    #               [1.164, 0.000, 1.596]])  # R
    # # Take the dot product with the matrix to produce BGR output, clamp the
    # # results to byte range and convert to bytes
    # BGR = YUV.dot(M.T).clip(0, 255).astype(np.uint8)
    # # Display the image with OpenCV
    # cv2.imshow('image', BGR)
    # cv2.waitKey(  # TODO: por waitKey time dinamico: aka ir buscar os FPS
    #     10000)  # I found that it works if i press the key whilst the window is in focus. If the command line is
    # # in focus then nothing happens;
    # # Its in milliseconds