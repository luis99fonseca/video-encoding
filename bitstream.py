class BitStream:
    def __init__(self):
        self.current_byte = None

    def read_bit(self, filename):
        with open(filename, 'rb') as fr:
            fr.readline()
            fr.readline()
            self.current_byte = fr.read(1)
            for i in range(8):
                print( (self.current_byte >> i) & 1 )

    def read_bits(self, n):
        pass 

    def write_bit(self):
        pass

    def write_bits(self, n):
        pass 

