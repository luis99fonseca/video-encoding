import logging
import cv2
import numpy as np
import time


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)

c_handler = logging.StreamHandler()
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(logging.Formatter('%(name)s | %(levelname)s ->: %(message)s'))

logger.addHandler(c_handler)
logger.propagate = False  # https://stackoverflow.com/a/19561320

class VideoPlayer:
    def __init__(self, filename):
        self.fileName = filename
        # self.filePointer = 0
        self.thisFile = None

        self.mediaFormat = None
        self.height = 0
        self.width = 0
        self.frames = None

    def openYUV(self):
        if not self.mediaFormat:
            # TODO: melhorar eficiencia, nao abrindo sempre
            self.thisFile = open(self.fileName, "rb")
            header = self.thisFile.readline().decode().split()
            logger.debug("Header: %s", header)
                                                                            # "Hardcoded", as 4:2:0 format doesn't come with its format explicitly
            self.mediaFormat = [int(n) for n in list(header[-1])[1:]] if len(header) == 7 else [4,2,0]
            self.width = int(header[1][1:])
            self.height = int(header[2][1:])
            # self.filePointer = self.thisFile.tell()
        else:
            logger.error("File already opened!!")

    def readFrame(self):
        if self.mediaFormat:
            # Note: here we are implying there are only these 3 formats, so that this "switch" can make sense
            if self.mediaFormat[-1] == 4:
                logger.debug("Frame (4,4,4): %s", self.thisFile.readline())
                # self.thisFile.read(self.width * self.height)
                # self.thisFile.read(self.width * self.height)
                # self.thisFile.read(self.width * self.height)

                # logger.debug("Read Line: %s", self.thisFile.tell())

                # heavily inspired from: https://raspberrypi.stackexchange.com/questions/28033/reading-frames-of-uncompressed-yuv-video-file
                fwidth = self.width  # (self.width + 31) // 32 * 32
                fheight = self.height  # (self.height + 15) // 16 * 16
                # Load the Y (luminance) data from the stream

                # A try/except block is extremely efficient if no exceptions are raised. Actually catching an exception is expensive.
                # Also: https://stackoverflow.com/a/7604717
                try:
                    Y = np.fromfile(self.thisFile, dtype=np.uint8, count=fwidth * fheight). \
                        reshape((fheight, fwidth))
                except:
                    cv2.destroyAllWindows()
                    return False

                # logger.debug("Read Y: %s", self.thisFile.tell())

                # Load the UV (chrominance) data from the stream, and double its size
                U = np.fromfile(self.thisFile, dtype=np.uint8, count=(fwidth) * (fheight)). \
                    reshape((fheight, fwidth)) \
                    # .repeat(2, axis=0).repeat(2, axis=1)
                # logger.debug("Read U: %s", self.thisFile.tell())

                V = np.fromfile(self.thisFile, dtype=np.uint8, count=(fwidth) * (fheight)). \
                    reshape((fheight, fwidth)) \
                    # .repeat(2, axis=0).repeat(2, axis=1)
                # logger.debug("Read V: %s", self.thisFile.tell())
                # Stack the YUV channels together, crop the actual resolution, convert to
                # floating point for later calculations, and apply the standard biases
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
                    15)  # I found that it works if i press the key whilst the window is in focus. If the command line is in focus then nothing happens
                # its in milliseconds
            elif self.mediaFormat[-1] == 2:
                logger.debug("Frame (4,2,2): %s", self.thisFile.readline())

                # self.thisFile.read(self.width * self.height)
                # self.thisFile.read(int(self.width * self.height / 2))
                # self.thisFile.read(int(self.width * self.height / 2))
                # logger.debug("Read Line: %s", self.thisFile.tell())

                # heavily inspired from: https://raspberrypi.stackexchange.com/questions/28033/reading-frames-of-uncompressed-yuv-video-file
                fwidth = self.width  # (self.width + 31) // 32 * 32
                fheight = self.height  # (self.height + 15) // 16 * 16
                # Load the Y (luminance) data from the stream

                # A try/except block is extremely efficient if no exceptions are raised. Actually catching an exception is expensive.
                # Also: https://stackoverflow.com/a/7604717
                try:
                    Y = np.fromfile(self.thisFile, dtype=np.uint8, count=fwidth * fheight). \
                        reshape((fheight, fwidth))
                except:
                    cv2.destroyAllWindows()
                    return False

                # logger.debug("Read Y: %s", self.thisFile.tell())

                # Load the UV (chrominance) data from the stream, and double its size
                U = np.fromfile(self.thisFile, dtype=np.uint8, count=(fwidth) * (fheight) // 2). \
                    reshape((fheight, fwidth // 2)) \
                    .repeat(2, axis=1)
                    # this format maintains the number of lines (so the reshape mantains them), thus we just need to \
                # repeat each collumn

                # logger.debug("Read U: %s", self.thisFile.tell())

                V = np.fromfile(self.thisFile, dtype=np.uint8, count=(fwidth) * (fheight) // 2). \
                    reshape((fheight, fwidth // 2)) \
                    .repeat(2, axis=1)

                # logger.debug("Read V: %s", self.thisFile.tell())
                # Stack the YUV channels together, crop the actual resolution, convert to
                # floating point for later calculations, and apply the standard biases
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
                    5)  # I found that it works if i press the key whilst the window is in focus. If the command line is in focus then nothing happens
                # its in milliseconds


            else:
                logger.debug("Frame (4,2,0): %s - %s", self.thisFile.readline(), "yolo")
                # self.thisFile.read(self.width * self.height)
                # self.thisFile.read(int(self.width * self.height / 4))
                # self.thisFile.read(int(self.width * self.height / 4))

                # heavily inspired from: https://raspberrypi.stackexchange.com/questions/28033/reading-frames-of-uncompressed-yuv-video-file
                fwidth = self.width  # (self.width + 31) // 32 * 32
                fheight = self.height  # (self.height + 15) // 16 * 16
                # Load the Y (luminance) data from the stream

                # A try/except block is extremely efficient if no exceptions are raised. Actually catching an exception is expensive.
                # Also: https://stackoverflow.com/a/7604717
                try:
                    Y = np.fromfile(self.thisFile, dtype=np.uint8, count=fwidth * fheight). \
                        reshape((fheight, fwidth))
                except:
                    cv2.destroyAllWindows()
                    return False

                # logger.debug("Read Y: %s", self.thisFile.tell())

                # Load the UV (chrominance) data from the stream, and double its size
                U = np.fromfile(self.thisFile, dtype=np.uint8, count=(fwidth) * (fheight) // 4). \
                    reshape((fheight // 2, fwidth // 2)) \
                    .repeat(2, axis=0).repeat(2, axis=1)
                # this format maintains the number of lines (so the reshape mantains them), thus we just need to \
                # repeat each collumn

                # logger.debug("Read U: %s", self.thisFile.tell())

                V = np.fromfile(self.thisFile, dtype=np.uint8, count=(fwidth) * (fheight) // 4). \
                    reshape((fheight // 2, fwidth // 2)) \
                    .repeat(2, axis=0).repeat(2, axis=1)

                # logger.debug("Read V: %s", self.thisFile.tell())
                # Stack the YUV channels together, crop the actual resolution, convert to
                # floating point for later calculations, and apply the standard biases
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
                    5)  # I found that it works if i press the key whilst the window is in focus. If the command line is in focus then nothing happens
                # its in milliseconds

            return True
        else:
            logger.error("File not opened yet!!")
            return False

    def __str__(self):
        return "VideoPlayer ( file= {}; format={}; height={}; width={} )".format(self.fileName, self.mediaFormat, self.height, self.width)

if __name__ == "__main__":
    videoPlayer01 = VideoPlayer("media/park_joy_420_720p50.y4m")
    videoPlayer01.openYUV()
    print(videoPlayer01)
    print("for more, see: https://wiki.multimedia.cx/index.php?title=YUV4MPEG2")
    i=0
    while (videoPlayer01.readFrame()):
        # print("i: ",i , sep="")
        # i+=1
        pass

    # (videoPlayer01.readFrame())


