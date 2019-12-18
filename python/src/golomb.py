import math


class Golomb:
    """
    This class implements the Golomb codification to compress information.
    It encodes an integer based on a given value of M. 
    The codification is the result of the concatenation of an unary code with a binary code,
    given by the quotient and remainder of the division between integer value and M, respectively.
    """
    def __init__(self, m=2):
        """
        The constructor.

        @param m: value of M (default = 2)
        """
        assert m > 0

        self.m = m

        # Check if M is a power of 2 or not
        self.base2 = True if math.log2(m).is_integer() else False

        # Initialization of two dictionary with encoded and decoded values from -255 to 255,
        # in order to avoid constant coding and decoding and increase performance
        self.encoded_values = {i:self.encode(i) for i in range(-255,256)}
        self.decoded_values = {''.join(str(bit) for bit in self.encoded_values[i]):i for i in range(-255,256)}

    def set_m(self, m):
        """
        This method updates the value of M.

        @param m: new M
        """
        assert m > 0

        self.m = m
        self.base2 = True if math.log2(m).is_integer() else False
    
    def encode(self, n):
        """
        This method, depending on the value of M, calls the respective method to encode the given value 'n'.
        If M is a power of two, it calls the base2encoder() method. Else, it calls the truncated_encoder() method.
        """
        return self.base2encoder(n) if self.base2 else self.truncated_encoder(n)

    def base2encoder(self, n):
        """
        This method encodes a given integer 'n' with Golomb encoding, using a power of two value of 'M'.

        @param n: integer to encode
        """
        
        # check 'n' sign (0 - positive, 1 - negative)
        sign = [0]  
        if n < 0:
            n = abs(n)
            sign = [1] 

        # computes values of 'q' and 'r'
        q = math.floor(n / self.m)
        r = n % self.m

        # computes unary and binary codes of 'q' and 'r', respectively.
        unary_code = [1 for i in range(q)] + [0]
        binary_code = [int(i) for i in list(bin(r))[2:]] if r >= 2 else [0] + [int(i) for i in list(bin(r))[2:]]
        
        # returns the golomb code of 'n'
        return  sign + unary_code + binary_code
    
    def truncated_encoder(self, n):
        """
        This method encodes a given integer 'n' with truncated Golomb encoding.

        @param n: integer to encode
        """

        # check 'n' sign (0 - positive, 1 - negative)
        sign = [0]
        if n < 0:
            n = abs(n)
            sign = [1]

        b = math.ceil(math.log2(self.m))

        q = math.floor(n / self.m)
        r = n % self.m
        
        unary_code = [1 for i in range(q)] + [0]

        first_values = 2**b - self.m
        if r < first_values:
            binary_code = self.decimal_to_binary(r, b - 1)
        else:
            binary_code = self.decimal_to_binary(r + 2**b - self.m, b)

        # return the truncated golomb code of 'n'
        return sign + unary_code + binary_code
    
    def stream_decoder(self, bitstream, i=0):
        """
        This method decodes a bitstream with multiple integers.
        Example: stream_decoder([0,0,0,1,0,0,1,0,0,0,0,0]) -> [1,2,0]

        @param bitstream: a list of bits
        """
        
        if not bitstream:
            return []

        # all decoded integers
        decoded = []

        # loop until all bits are decoded
        while True:
            sign = bitstream[i]
            i+=1

            if bitstream[i] == 0:   # current code < self.m -1
                unary_code = [bitstream[i]]
                i += 1
                binary_code = bitstream[i:(i + math.ceil(math.sqrt(self.m)))]
                i += math.ceil(math.sqrt(self.m))
                decimal = self.decoded_values[''.join(str(bit) for bit in [sign] + unary_code + binary_code)]
                decoded.append(decimal)

            else:   # currente code >= self.m - 1
                unary_code = []
                while True:
                    bit = bitstream[i]
                    unary_code.append(bit)
                    i += 1
                    if bit == 0:
                        break
                binary_code = bitstream[i:i + math.ceil(math.sqrt(self.m))]
                i += math.ceil(math.sqrt(self.m))
                decimal = self.decoded_values[''.join(str(bit) for bit in [sign] + unary_code + binary_code)]
                decoded.append(decimal)
            
            if i >= len(bitstream):
                break

        return decoded

    def decode(self, bitstream):
        """
        This method, depending on the value of M, calls the respective method to decode a given list of bits.
        If M is a power of two, it calls the base2decoder() method. Else, it calls the truncated_decoder() method.

        @param bitstream: list of bits to decode
        """
        assert len(bitstream) > 0
        return self.base2decoder(bitstream) if self.base2 else self.truncated_decoder(bitstream)

    def base2decoder(self, bitstream):
        """
        This method decodes a given list of bits, encoded with Golomb encoding.

        @param bitstream: list of bits to decode
        """
        
        negative = bitstream[0] == 1
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
        """
        This method decodes a given list of bits, encoded with truncated Golomb encoding.

        @param bitstream: list of bits to decode
        """
        negative = bitstream[0] == 1
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

    def decimal_to_binary(self, decimal, bits):
        """
        This method, given a natural number, converts it into base2 with a given number of bits.
        """
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
        """
        This method, given a base2 number, converts it into a natural number.
        """
        return sum([int(binary[i]) * 2**(len(binary) - 1 - i) for i in range(len(binary))])
    
    def frequency(self, text):
        """
        This method, given a set of symbols in 'text', computes the frequency of each symbol.
        """
        frequency = dict()

        for symbol in text:
            if symbol not in frequency:
                frequency[symbol] = 1
            else:
                 frequency[symbol] += 1

        frequency = sorted(frequency.items(), reverse=True, key=lambda kv: kv[1])
        self.histogram = [(f[0], f[1] / len(text)) for f in frequency]
        return self.histogram
