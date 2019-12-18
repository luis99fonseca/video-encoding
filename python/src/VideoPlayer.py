from frames import *
import cv2
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)

c_handler = logging.StreamHandler()
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(logging.Formatter('%(name)s | %(levelname)s ->: %(message)s'))

logger.addHandler(c_handler)
logger.propagate = False  # https://stackoverflow.com/a/19561320

class VideoPlayer:
    """
    This class implements a video player.
    It reads a file in 'y4m' format and display it on a window, frame by frame.
    """
    def __init__(self, filename):
        self.fileName = filename
        # self.filePointer = 0

        self.mediaFormat = None
        self.height = 0
        self.width = 0
        self.frame = None

    def openYUV(self):
        if not self.mediaFormat:
            with open(self.fileName, "rb") as temp_file:
                header = temp_file.readline().decode().split()
                logger.debug("Header: %s", header)

            # "Hardcoded", as 4:2:0 format doesn't come with its format explicitly
            self.mediaFormat = [int(n) for n in list(header[-1])[1:]] if len(header) == 7 else [4, 2, 0]
            self.width = int(header[1][1:])
            self.height = int(header[2][1:])

            if self.mediaFormat[-1] == 4:
                self.frame = Frame444(self.height, self.width, self.fileName)
            elif self.mediaFormat[-1] == 2:
                self.frame = Frame422(self.height, self.width, self.fileName)
            else:
                self.frame = Frame420(self.height, self.width, self.fileName)

        else:
            logger.error("File already opened!!")

    def readFrame(self):
        """
        This method, as its name suggest, reads one frame from a video and displays it in a window.
        """
        if self.mediaFormat:

            if not self.frame.advance():
                cv2.destroyAllWindows()
                return False

            Y = self.frame.getY()

            U = self.frame.getU()

            V = self.frame.getV()

            # Note: here we are implying that there are only these 3 formats, so that this "if" can make sense
            if self.mediaFormat[-1] == 2:
                # logger.debug("Frame (4,2,2): ")

                # Gets the UV (chrominance) data from the Frame, and double its size;
                # This format maintains the number of lines (so the reshape keeps them), thus we just need to \
                # repeat each column
                U = U.repeat(2, axis=1)

                V = V.repeat(2, axis=1)

            elif self.mediaFormat[-1] == 0:
                # logger.debug("Frame (4,2,0): ")

                U = U.repeat(2, axis=0).repeat(2, axis=1)

                V = V.repeat(2, axis=0).repeat(2, axis=1)

            YUV = np.dstack((Y, U, V))[:self.height, :self.width, :].astype(np.float)
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
            cv2.waitKey(    # TODO: por waitKey time dinamico: aka ir buscar os FPS
                21)  # I found that it works if i press the key whilst the window is in focus. If the command line is
            # in focus then nothing happens;
            # Its in milliseconds

            return True
        else:
            logger.error("File not opened yet!!")
            return False

    def __str__(self):
        return "VideoPlayer ( file= {}; Frame={}; height={}; width={} )".format(self.fileName, self.frame,
                                                                                 self.height, self.width)


if __name__ == "__main__":
    videoPlayer01 = VideoPlayer("../media/park_joy_444_720p50.y4m")
    videoPlayer01.openYUV()
    print(videoPlayer01)

    print("for more, see: https://wiki.multimedia.cx/index.php?title=YUV4MPEG2")
    while (videoPlayer01.readFrame()):
        pass
