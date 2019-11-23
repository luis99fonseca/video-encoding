import math

class Golomb:
    def __init__(self, m):
        assert m > 0
        self.m = m

    def encode(self, n):
        assert n >= 0

        q = self.quocient(n, self.m)
        r = self.remainder(n, self.m)

        unary_code = self.unary_code(q)
        binary_code = self.decimal_to_binary(r)

        golomb_code = unary_code + binary_code
        s = ''
        return s.join(golomb_code)

    def decode(self, bitstream):
        bitstream = str(bitstream)

        if bitstream[0] == '0':
            q = 0
            r = self.binary_to_decimal(bitstream[1:])
        else:
            i = 0
            while bitstream[i] == '1':
                i += 1
            
            unary_code = bitstream[0:i+1]
            binary_code = bitstream[i+1:]
            
            q = i
            r = self.binary_to_decimal(binary_code)

        return r + q * self.m

    def quocient(self, n, m):
        return math.floor(n / m)

    def remainder(self, n, m):
        return n % m
    
    def unary_code(self, q):
        return [str(1) for i in range(q)] + ['0']
    
    def decimal_to_binary(self, decimal):
        binary = []
        n = decimal
        while True:
            q = math.floor(n / 2)
            bit = n - q * 2
            binary.append(str(bit))
            n = q
            if q == 0:
                break
        return binary
    
    def binary_to_decimal(self, binary):
        return sum([int(binary[i]) * 2**i for i in range(len(binary))])

if __name__ == '__main__':
    golomb = Golomb(4)
    
    print("Encoding")
    codes = []
    for i in range(15):
        codes.append(golomb.encode(i))
        print(codes[i])
    
    print("Decoding")
    for i in range(15):
        print(golomb.decode(codes[i]))