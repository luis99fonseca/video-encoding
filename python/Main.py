from Frames import *
from bitstream.BitStream import *
from encoding.Predictors import *
from encoding.Encoders import *
from golomb.Golomb import *
from VideoPlayer import *
import numpy as np

print("------Frame------")
f = Frame444(1280, 720,"media/park_joy_444_720p50.y4m")
f.advance()
matrix2 = f.getY()

print("------BitStream------")
b = BitStream("media/park_joy_444_720p50.y4m")

print("------Encoders & Predictors------")
en = IntraFrameEncoder(matrix2, "Y", [4,4,4], JPEG1)
en.encode()

