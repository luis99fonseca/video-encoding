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
    Class that implements a video player.
    It reads a file in 'y4m' format and display it on a window, frame by frame.
    """
    def __init__(self, filename=None, fromFile=True):
        self.fileName = filename
        # self.filePointer = 0

        self.mediaFormat = None
        self.height = 0
        self.width = 0
        self.frame = None

        self.spf = 1

        self.fromFile = fromFile
        self.arrayStream = None
        self.videoIndex = 0

    def openYUV(self):
        """
        Function used to read the header from a file, to get the basic video info from it
        """
        if not self.mediaFormat and self.fromFile:
            with open(self.fileName, "rb") as temp_file:
                header = temp_file.readline().decode().split()
                logger.debug("Header: %s", header)

            # "Hardcoded", as 4:2:0 format doesn't come with its format explicitly
            self.mediaFormat = [int(n) for n in list(header[-1])[1:]] if len(header) == 7 else [4, 2, 0]
            self.width = int(header[1][1:])
            self.height = int(header[2][1:])

            # reverse of fps, relevant for imshow timing, which is in seconds
            self.spf = 1000 // int(header[3].split(":")[0].split("F")[1])

            if self.mediaFormat[-1] == 4:
                self.frame = Frame444(self.height, self.width, self.fileName)
            elif self.mediaFormat[-1] == 2:
                self.frame = Frame422(self.height, self.width, self.fileName)
            else:
                self.frame = Frame420(self.height, self.width, self.fileName)

        else:
            logger.error("File already opened!!")

    def openInfo(self, info, videoData):
        """
        Function to get the basic video info so it can display

        @param info: tuple with data as follow (height, width, formatType, fps), all shall be integer
        @param videoData: array with decoded matrices
        @return:
        """
        if not self.fromFile:
            self.height = info[0]
            self.width = info[1]
            if info[2] == 444:
                self.frame = "444"
                self.mediaFormat = "444"
            elif info[2] == 422:
                self.frame = "422"
                self.mediaFormat = "422"
            elif info[2] == 420:
                self.frame = "420"
                self.mediaFormat = "420"
            self.spf = 1000 // info[3]
            self.arrayStream = videoData
        else:
            logger.error("Player not defined as arrayReader!!")

    def visualizeFrame(self):
        """
        This method, as its name suggest, reads one frame from a video and displays it in a window.
        """
        if self.mediaFormat:
            if self.fromFile:

                if not self.frame.advance():
                    cv2.destroyAllWindows()
                    return False

                Y = self.frame.getY()

                U = self.frame.getU()

                V = self.frame.getV()

            else:
                if self.videoIndex < len(self.arrayStream):
                    Y = self.arrayStream[self.videoIndex]
                    U = self.arrayStream[self.videoIndex + 1]
                    V = self.arrayStream[self.videoIndex + 2]

                    self.videoIndex += 3
                else:
                    logger.info("End of video Stream!!")
                    return False

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
            cv2.waitKey(
                self.spf)  # I found that it works if i press the key whilst the window is in focus. If the command line is
            # in focus then nothing happens;
            # Its in milliseconds

            return True
        else:
            logger.error("Info not oppened yet!!")
            return False

    def __str__(self):
        return "VideoPlayer ( file= {}; Frame={}; height={}; width={} )".format(self.fileName, self.frame,
                                                                                 self.height, self.width)


if __name__ == "__main__":
    videoPlayer01 = VideoPlayer("../media/park_joy_444_720p50.y4m")
    videoPlayer01.openYUV()
    
    print("for more, see: https://wiki.multimedia.cx/index.php?title=YUV4MPEG2")
    while (videoPlayer01.visualizeFrame()):
        pass
