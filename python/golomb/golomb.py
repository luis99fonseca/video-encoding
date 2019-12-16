import math

class Golomb:
    def __init__(self, m=2):
        assert m > 0

        self.m = m
        self.base2 = True if math.log2(m).is_integer() else False

    def set_m(self, m):
        assert m > 0

        self.m = m
        self.base2 = True if math.log2(m).is_integer() else False

    def encode(self, n):
        return self.base2encoder(n) if self.base2 else self.truncated_encoder(n)

    def base2encoder(self, n):
        
        negative = [0]
        if n < 0:
            n = abs(n)
            negative = [1]

        q = self.quocient(n, self.m)
        r = self.remainder(n, self.m)

        unary_code = self.unary_code(q)
        binary_code = self.decimal_to_binary(r, 2)

        golomb_code = unary_code + binary_code
        return negative + golomb_code
    
    def truncated_encoder(self, n):
        negative = [0]
        if n < 0:
            n = abs(n)
            negative = [1]

        b = math.ceil(math.log2(self.m))

        q = self.quocient(n, self.m)
        r = self.remainder(n, self.m)
        
        unary_code = self.unary_code(q)

        first_values = 2**b - self.m
        if r < first_values:
            binary_code = self.decimal_to_binary(r, b - 1)
        else:
            binary_code = self.decimal_to_binary(r + 2**b - self.m, b)
        
        golomb_code = unary_code + binary_code

        return negative + golomb_code
    
    def stream_decoder(self, bitstream):
        decoded = []
        while True:
            sign = bitstream[0]
            bitstream = bitstream[1:]

            if bitstream[0] == 0:
                unary_code = [bitstream[0]]
                binary_code = bitstream[1:(1 + math.ceil(math.sqrt(self.m)))]
                decimal = self.decode([sign] + unary_code + binary_code)
                decoded.append(decimal)
                bitstream = bitstream[(1 + math.ceil(math.sqrt(self.m))):]
                if not bitstream:
                    break
            else:
                unary_code = []
                while True:
                    bit = bitstream.pop(0)
                    unary_code.append(bit)
                    if bit == 0:
                        break
                binary_code = bitstream[0:math.ceil(math.sqrt(self.m))]
                decimal = self.decode([sign] + unary_code + binary_code)
                decoded.append(decimal)
                bitstream = bitstream[math.ceil(math.sqrt(self.m)):]
                if not bitstream:
                    break

        return decoded

    
    def decode(self, bitstream):
        assert len(bitstream) > 0
        return self.base2decoder(bitstream) if self.base2 else self.truncated_decoder(bitstream)

    def isNegative(self, bitstream):
        return bitstream[0] == 1

    def base2decoder(self, bitstream):
        
        negative = self.isNegative(bitstream)
        bitstream = bitstream[1:]

        if bitstream[0] == 0:
            q = 0
            r = self.binary_to_decimal(bitstream[1:])
        else:
            i = 0
            while bitstream[i] == 1:
                i += 1
            
            unary_code = bitstream[0:i+1]
            binary_code = bitstream[i+1:]
            
            q = i
            r = self.binary_to_decimal(binary_code)

        return r + q * self.m if not negative else -1 * (r + q * self.m)
    
    def truncated_decoder(self, bitstream):
        negative = self.isNegative(bitstream)
        bitstream = bitstream[1:]

        b = math.ceil(math.log2(self.m))

        if bitstream[0] == 0:
            q = 0
            binary_code = bitstream[1:]
        else:
            i = 0
            while bitstream[i] == 1:
                i += 1

            q = i
            binary_code = bitstream[i:]

        first_values = 2**b - self.m
        decimal = self.binary_to_decimal(binary_code)
        if decimal < first_values:
            return decimal + q * self.m if not negative else -1 * (decimal + q * self.m)
        else:
            return decimal + self.m - 2**b + q * self.m if not negative else -1 * (decimal + self.m - 2**b + q * self.m)

    def quocient(self, n, m):
        return math.floor(n / m)

    def remainder(self, n, m):
        return n % m
    
    def unary_code(self, q):
        return [1 for i in range(q)] + [0]
    
    def decimal_to_binary(self, decimal, bits):
        binary = []
        n = decimal
        while True:
            q = math.floor(n / 2)
            bit = n % 2
            binary.append(bit)
            n = q
            if q == 0:
                break
        
        binary = binary[::-1]
        if len(binary) < bits:
            binary = [0 for i in range(bits - len(binary))] + binary        
        return binary
    
    def binary_to_decimal(self, binary):
        return sum([int(binary[i]) * 2**(len(binary) - 1 - i) for i in range(len(binary))])
    
    def histogram(self, text):
        frequency = dict() 

        for symbol in text:
            if symbol not in frequency:
                frequency[symbol] = 1
            else:
                 frequency[symbol] += 1

        frequency = sorted(frequency.items(), reverse=True, key=lambda kv: kv[1])
        self.histogram = [(f[0], f[1] / len(text)) for f in frequency]
        return self.histogram


if __name__ == '__main__':
    golomb = Golomb(4)

    print(golomb.stream_decoder([0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,1,0,1,0,0,0,0,1,0,0,1,0,1,0,1,0,0,1,0,1,1,0,1,1,0,0,0,0,1,1,0,0,1,0,1,1,0,1,0,0,1,1,0,1,1,0,1,1,1,0,0,0,0,1,1,1,0,0,1,0,1,1,1,0,1,1,0,1,1,1,0,1,0]))