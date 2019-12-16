from BitStream import BitStream
from golomb import Golomb 

if __name__ == '__main__':
    golomb = Golomb(4)
    a = golomb.load_golomb_codes()
    bitstream = BitStream("./predictor.bin", "rb")
    print(bitstream.readString())
    codes = []
    while True:
        bit = bitstream.readBit(1)
        if not bit:
            break 
        codes += bit
    
    c = []
    b = codes
    while True:
        decoded, b = golomb.stream_decoder(b)
        c.append(decoded)
        if not b or len(c) > 720:
            break
        print(decoded)