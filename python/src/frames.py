from abc import ABC, abstractmethod
import logging
import numpy as np

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)

c_handler = logging.StreamHandler()
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(logging.Formatter(
    '%(name)s | %(levelname)s ->: %(message)s'))

logger.addHandler(c_handler)
logger.propagate = False  # https://stackoverflow.com/a/19561320


class Frame(ABC):
    """
    Abstract class of a Frame.
    """
    def __init__(self, height, width, fileName):
        self.height = height
        self.width = width

        self.YComponent = None
        self.UComponent = None
        self.VComponent = None

        # so that we advance past the header
        self.file = open(fileName, "rb")
        self.file.readline()

    @abstractmethod
    def advance(self):
        """
        Advances and consumes the current bunch of data, so that it can refresh the current set of matrices with new
        ones.
        :return whether or not the reading (and setting operation was successful)
        """
        pass

    @abstractmethod
    def getY(self):
        return self.YComponent

    @abstractmethod
    def getU(self):
        return self.UComponent

    @abstractmethod
    def getV(self):
        return self.VComponent


class Frame444(Frame):
    """
    This class, derived from 'Frame', implements a 4:4:4 frame.
    """
    def __init__(self, height, width, fileName):
        super().__init__(height, width, fileName)

    def advance(self):

        # so that it reads past the line with the "FRAME" flag
        self.file.readline()

        # A try/except block is extremely efficient if no exceptions are raised. Actually catching an exception is
        # expensive. Also: https://stackoverflow.com/a/7604717
        try:
            self.YComponent = np.fromfile(self.file, dtype=np.uint8, count=self.width * self.height). \
                reshape((self.height, self.width))

        except Exception as e:  # todo, por aqui o erro que se tem em EOF, e outro except para o resto deles
            logger.error(e)
            self.file.close()
            return False

        self.UComponent = np.fromfile(self.file, dtype=np.uint8, count=self.width * self.height). \
            reshape((self.height, self.width))

        self.VComponent = np.fromfile(self.file, dtype=np.uint8, count=self.width * self.height). \
            reshape((self.height, self.width))

        return True

    def getY(self):
        return super().getY()

    def getU(self):
        return super().getU()

    def getV(self):
        return super().getV()

    def __str__(self):
        return "Frame ( format= {}; height={}; width={} )".format("444", self.height, self.width)


class Frame422(Frame):
    """
    This class, derived from 'Frame', implements a 4:2:2 frame.
    """
    def __init__(self, height, width, fileName):
        super().__init__(height, width, fileName)

    def advance(self):

        # so that it reads past the line with the "FRAME" flag
        self.file.readline()

        # A try/except block is extremely efficient if no exceptions are raised. Actually catching an exception is
        # expensive. Also: https://stackoverflow.com/a/7604717
        try:
            self.YComponent = np.fromfile(self.file, dtype=np.uint8, count=self.width * self.height). \
                reshape((self.height, self.width))
        except Exception as e:  # todo, por aqui o erro que se tem em EOF, e outro except para o resto deles
            logger.error(e)
            self.file.close()
            return False

        self.UComponent = np.fromfile(self.file, dtype=np.uint8, count=self.width * self.height // 2). \
            reshape((self.height, self.width // 2))

        self.VComponent = np.fromfile(self.file, dtype=np.uint8, count=self.width * self.height // 2). \
            reshape((self.height, self.width // 2))

        return True

    def getY(self):
        return super().getY()

    def getU(self):
        return super().getU()

    def getV(self):
        return super().getV()

    def __str__(self):
        return "Frame ( format= {}; height={}; width={} )".format("422", self.height, self.width)


class Frame420(Frame):
    """
    This class, derived from 'Frame', implements a 4:2:0 frame.
    """
    def __init__(self, height, width, fileName):
        super().__init__(height, width, fileName)

    def advance(self):

        # so that it reads past the line with the "FRAME" flag
        self.file.readline()

        # A try/except block is extremely efficient if no exceptions are raised. Actually catching an exception is
        # expensive. Also: https://stackoverflow.com/a/7604717
        try:
            self.YComponent = np.fromfile(self.file, dtype=np.uint8, count=self.width * self.height). \
                reshape((self.height, self.width))
        except Exception as e:  # todo, por aqui o erro que se tem em EOF, e outro except para o resto deles
            logger.error(e)
            self.file.close()
            return False

        self.UComponent = np.fromfile(self.file, dtype=np.uint8, count=self.width * self.height // 4). \
            reshape((self.height // 2, self.width // 2))

        self.VComponent = np.fromfile(self.file, dtype=np.uint8, count=self.width * self.height // 4). \
            reshape((self.height // 2, self.width // 2))

        return True

    def getY(self):
        return super().getY()

    def getU(self):
        return super().getU()

    def getV(self):
        return super().getV()

    def __str__(self):
        return "Frame ( format= {}; height={}; width={} )".format("420", self.height, self.width)
