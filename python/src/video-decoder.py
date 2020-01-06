import numpy as np
import datetime
import logging
import predictors
from bitStream import BitStream
from golomb import Golomb
from frames import *
from encoders import IntraFrameDecoder
from VideoPlayer import VideoPlayer
import cv2
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('root')
logger.setLevel(logging.ERROR)

c_handler = logging.StreamHandler()
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(logging.Formatter('%(name)s | %(levelname)s ->: %(message)s'))

logger.addHandler(c_handler)
logger.propagate = False  # https://stackoverflow.com/a/19561320

"""
This program decodes a 3 frames video. 
"""
if __name__ == '__main__':

    bitstream = BitStream("../out/3_frames_encoded_park_joy_444_720p50.bin", "rb")
    golomb = Golomb(4)

    # read header
    no_frames, height, width, formatC0, fps0 = bitstream.readString().split("\t")
    print(no_frames, height, width)
    no_frames, height, width, formatC1, fps1 = int(no_frames[1:]), int(height[1:]), int(width[1:]), int(formatC0[1:]), int(fps0[1:])
    
    matrixes = 0
    frames = 0
    decoded_matrixes = []
    stream = []
    total_time = 0
    start = datetime.datetime.now()
    while frames < no_frames:

        stream += bitstream.readBit(height*width*8)
        decoded, i = golomb.stream_decoder(stream, height*width)
        stream = stream[i:]
        matrixes += 1

        decoded = np.array(decoded, dtype=np.int16).reshape((height,width))
        intraFrameDecoder = IntraFrameDecoder(decoded, predictors.JPEG1)
        intraFrameDecoder.decode()
        decoded_matrixes.append(intraFrameDecoder.decoded_matrix)
        if matrixes % 3 == 0:
            end = datetime.datetime.now() - start
            frames += 1
            total_time += end.seconds
            print("Frame decompressed in {} s. Frames no. {}".format(end.seconds, frames))
            start = datetime.datetime.now()
        
        if i == 0: # EOF
            break

        # Comment/Uncomment this line
        if frames == 3:
            break

    bitstream.closeFile()
    print("Video decoded with success!")




    if True:
        info = (height, width, formatC1, fps1)
        videoPlayer01 = VideoPlayer(fromFile=False)
        videoPlayer01.openInfo(info, decoded_matrixes)

        while (videoPlayer01.visualizeFrame()):
            pass
    # Code bellow, altho very hardcoded, shows the up to 3 frame, so we can check whether things went well or not
    if False:
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
        cv2.waitKey(
            1000 // fps1)
        Y = decoded_matrixes[3]
        U = decoded_matrixes[4]
        V = decoded_matrixes[5]
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
        cv2.waitKey(
            1000 // fps1)
        Y = decoded_matrixes[6]
        U = decoded_matrixes[7]
        V = decoded_matrixes[8]
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
        cv2.waitKey(
            1000 // fps1)