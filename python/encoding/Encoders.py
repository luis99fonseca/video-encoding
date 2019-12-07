import numpy as np
import time
import Predictors
import logging

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
        self.encoded_matrix = np.empty(self.original_matrix.shape)

    def encode(self):
        if not self.type:
            logger.error("Matrix Type {} not valid; Must be one of ['Y', 'U', 'V']. Aborting.".format(self.type))
            return False
        if self.format == [4,4,4]:
            # matrix size/shape is the same no mather which one

            self.encoded_matrix[0, 0] = self.predictor()

            for col in range(1, self.original_matrix.shape[0]):
                self.encoded_matrix[col, 0] = self.predictor.predict()

            for col in range(self.original_matrix.shape[0]):
                for line in range(self.original_matrix.shape[0]):



if __name__ == "__main__":
    matrix = np.empty([1280,720])
    print(matrix.shape[0])
    matrix[1,1] = 1
    print(matrix)
    ife = IntraFrameEncoder(matrix, "Y", [4,4,4], Predictors.JPEG1)

