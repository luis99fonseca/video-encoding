from golomb import Golomb
import random

if __name__ == '__main__':
    golomb = Golomb(4)

    codes = [random.randint(-255, 255) for i in range(921600)]

    encoded = [golomb.encode(code) for code in codes]

    print(encoded)


