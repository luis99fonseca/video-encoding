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
                self.thisFile.read(self.width * self.height)
                self.thisFile.read(self.width * self.height)
                self.thisFile.read(self.width * self.height)
            elif self.mediaFormat[-1] == 2:
                logger.debug("Frame (4,2,2): %s", self.thisFile.readline())
                self.thisFile.read(self.width * self.height)
                self.thisFile.read(int(self.width * self.height / 2))
                self.thisFile.read(int(self.width * self.height / 2))
            else:
                logger.debug("Frame (4,2,0): %s", self.thisFile.readline())
                self.thisFile.read(self.width * self.height)
                self.thisFile.read(int(self.width * self.height / 4))
                self.thisFile.read(int(self.width * self.height / 4))
        else:
            logger.error("File not opened yet!!")

    def __str__(self):
        return "VideoPlayer ( file= {}; format={}; height={}; width={} )".format(self.fileName, self.mediaFormat, self.height, self.width)

if __name__ == "__main__":
    videoPlayer01 = VideoPlayer("media/park_joy_422_720p50.y4m")
    videoPlayer01.openYUV()
    print(videoPlayer01)
    print("for more, see: https://wiki.multimedia.cx/index.php?title=YUV4MPEG2")
    (videoPlayer01.readFrame())
    (videoPlayer01.readFrame())