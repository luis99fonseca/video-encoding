class VideoPlayer:
    def __init__(self, filename):
        self.fileName = filename

        self.mediaFormat = None
        self.height = 0
        self.width = 0
        self.frames = None

    def openYUV(self):
        if self.mediaFormat is None:
            # TODO: melhorar eficiencia, nao abrindo sempre
            with open(self.fileName, "rb") as temp_file:
                header = temp_file.readline().decode().split()
                self.mediaFormat = [int(n) for n in list(header[-1])[1:]]
                self.width = int(header[1][1:])
                self.height = int(header[2][1:])

                print(">>", temp_file.readline())
                temp_file.read(self.width * self.height)
                temp_file.read(self.width * self.height)
                temp_file.read(self.width * self.height)
                print(">>", temp_file.readline())

    def __str__(self):
        return "VideoPlayer ( file= {}; format={}; height={}; width={} )".format(self.fileName, self.mediaFormat, self.height, self.width)

if __name__ == "__main__":
    videoPlayer01 = VideoPlayer("media/park_joy_444_720p50.y4m")
    videoPlayer01.openYUV()
    print("---")
    print(videoPlayer01)
    print("for more, see: https://wiki.multimedia.cx/index.php?title=YUV4MPEG2")