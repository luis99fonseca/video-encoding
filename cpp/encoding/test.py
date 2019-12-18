import random
from golomb import Golomb 

if __name__ == '__main__':
    golomb = Golomb(4)

    n = [random.randint(-255,255) for i in range(50)]
    codes = []
    for i in n:
        codes += golomb.encode(i)
    
    decoded = golomb.stream_decoder(codes)

    for i in range(len(n)):
        print(n[i], decoded[i])
    