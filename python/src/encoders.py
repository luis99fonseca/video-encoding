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
    def __init__(self, matrix, predictor):
        """
        Default constructor.

        @param matrix: initial matrix
        @param predictor: linear predictor
        """
        self.original_matrix = matrix
        self.predictor = predictor
        self.encoded_matrix = np.empty(self.original_matrix.shape)  # sighly faster
        print(">> ", matrix.shape)
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
        self.codes = []
    
    def encode(self):
        """
        This method encodes the original matrix in a new one, based on the current predictor.
        It also uses golomb codification for the entropy encoding.
        """

        # TODO: ver o que é aquele K do stor
        # write header with bitstream
        #self.bitstream.writeString("{}\t{}".format(self.original_matrix.shape[0],self.original_matrix.shape[1]))

        # matrix size/shape is the same no mather which one
        self.encoded_matrix[0, 0] = int(self.original_matrix[0,0] - self.predictor.predict(0,0,0))
        # self.codes += self.golomb.encoded_values[self.encoded_matrix[0, 0]]

        for col in range(1, self.original_matrix.shape[1]):
            self.encoded_matrix[0, col] = int(self.original_matrix[0, col]) - self.predictor.predict(self.original_matrix[0, col -1], 0, 0)
            # self.codes += self.golomb.encoded_values[self.encoded_matrix[0, col]]

        for line in range(1, self.original_matrix.shape[0]):
            self.encoded_matrix[line, 0] = int(self.original_matrix[line, 0]) - self.predictor.predict(0, self.original_matrix[line - 1, 0], 0)
            # self.codes += self.golomb.encoded_values[self.encoded_matrix[line, 0]]

        for line in range(1, self.original_matrix.shape[0]):
            for col in range(1, self.original_matrix.shape[1]):
               self.encoded_matrix[line, col] = int(self.original_matrix[line, col]) - self.predictor.predict(
                    self.original_matrix[line, col - 1], self.original_matrix[line - 1, col], self.original_matrix[line - 1, col -1])
               # self.codes += self.golomb.encoded_values[self.encoded_matrix[line, col]]

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
    # codes = []
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
        codes.append(ife.codes)
        print("Encoded Matrix 'Y': {}".format(ife.encoded_matrix))

        # encode U matrix
        matrix = frame.getU()
        print("Matrix 'U': {}".format(matrix))
        # ife = IntraFrameEncoder(matrix, predictors.JPEG1)
        ife.setMatrix(matrix)
        ife.encode()
        codes.append(ife.codes)
        # print("Encoded Matrix 'U': {}".format(ife.encoded_matrix))

        # encode V matrix
        matrix = frame.getV()
        print("Matrix 'V': {}".format(matrix))
        # ife = IntraFrameEncoder(matrix, predictors.JPEG1)
        ife.setMatrix(matrix)
        ife.encode()
        codes.append(ife.codes)
        print("Encoded Matrix 'V': {}".format(ife.encoded_matrix))

        end = datetime.datetime.now() - start
        print("Compressed frame in {} s. Total bits: {}".format(end.seconds, ife.written_bits))
        total += end.seconds
         # com este break só codifica um frame
        break
    ife.bitstream.closeFile()
    print("Compressed frames in {} s.".format(total))
    # while True:
    #     start = datetime.datetime.now()
    #     playing = frame.advance()
    #     if not playing:
    #         break
    #
    #     # encode Y matrix
    #     matrix = frame.getY()
    #     # print("Matrix 'Y': {}".format(matrix))
    #     ifeY = IntraFrameEncoder(matrix, predictors.JPEG1)
    #     # ifeY.encode()
    #     # codes.append(ife.codes)
    #     # print("Encoded Matrix 'Y': {}".format(ifeY.encoded_matrix))
    #
    #     # encode U matrix
    #     matrix = frame.getU()
    #     # print("Matrix 'U': {}".format(matrix))
    #     ifeU = IntraFrameEncoder(matrix, predictors.JPEG1)  # ife.setMatrix(matrix)
    #     # ifeU.encode()
    #     # codes.append(ifeU.codes)
    #     # print("Encoded Matrix 'U': {}".format(ifeU.encoded_matrix))
    #
    #     # encode V matrix
    #     matrix = frame.getV()
    #     # print("Matrix 'V': {}".format(matrix))
    #     ifeV = IntraFrameEncoder(matrix, predictors.JPEG1)  # ife.setMatrix(matrix)
    #     # ifeV.encode()
    #     # codes.append(ifeV.codes)
    #     # print("Encoded Matrix 'V': {}".format(ifeV.encoded_matrix))
    #
    #     tY = threading.Thread(name='Y-thread', target=ifeY.encode)
    #     tU = threading.Thread(name='U-thread', target=ifeU.encode)
    #     tV = threading.Thread(name='V-thread', target=ifeV.encode)
    #
    #     tY.start()
    #     tU.start()
    #     tV.start()
    #
    #     tY.join()
    #     tU.join()
    #     tV.join()
    #
    #     end = datetime.datetime.now() - start
    #     print("Compressed frame in {} s. Total bits: {}".format(end.seconds, 0))
    #     # print(ifeY.codes)
    #     total += end.seconds
    #     break  # com este break só codifica um frame
    # ife.bitstream.closeFile()


    # sys.exit(-1)
    decoded_matrixes = []
    ife.bitstream = BitStream("../out/encoded_park_joy_444_720p50.bin", "rb")
    for code in codes:
        # print("code: ", code)
        decoded = ife.golomb.stream_decoder(code)
        decoded = np.array(decoded, dtype=np.int16).reshape((720,1280))
        print("Decoded: {}".format(decoded))
        ifd = IntraFrameDecoder(decoded, predictors.JPEG1)
        ifd.decode()
        decoded_matrixes.append(ifd.decoded_matrix) # UTILIZA ESTA LISTA COM AS MATRIZES PARA DAR DISPLAY
        print("Original matrix: {}".format(ifd.decoded_matrix))

    # sys.exit(-1)
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

    
