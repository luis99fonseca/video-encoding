from golomb import Golomb

if __name__ == '__main__':
    golomb = Golomb()

    print("------------------------------")
    print("FIRST TEST - ENCODE WITH M = 4")
    print("------------------------------")

    golomb.m = 4

    codes = ["00", "01", "010", "011", "100", "101", "1010", "1011", "1100", "1101", "11010", "11011", "11100", "11101", "111010", "111011"]
    assert golomb.encode(0) == codes[0]
    assert golomb.encode(1) == codes[1]
    assert golomb.encode(2) == codes[2]
    assert golomb.encode(3) == codes[3]
    assert golomb.encode(4) == codes[4]
    assert golomb.encode(5) == codes[5]
    assert golomb.encode(6) == codes[6]
    assert golomb.encode(7) == codes[7]
    assert golomb.encode(8) == codes[8]
    assert golomb.encode(9) == codes[9]
    assert golomb.encode(10) == codes[10]
    assert golomb.encode(11) == codes[11]
    assert golomb.encode(12) == codes[12]
    assert golomb.encode(13) == codes[13]
    assert golomb.encode(14) == codes[14]
    assert golomb.encode(15) == codes[15]

    print("First test finished with success!")

    print("\n-------------------------------")
    print("SECOND TEST - DECODE WITH M = 4")
    print("-------------------------------")

    assert golomb.decode(codes[0]) == 0
    assert golomb.decode(codes[1]) == 1
    assert golomb.decode(codes[2]) == 2
    assert golomb.decode(codes[3]) == 3
    assert golomb.decode(codes[4]) == 4
    assert golomb.decode(codes[5]) == 5
    assert golomb.decode(codes[6]) == 6
    assert golomb.decode(codes[7]) == 7
    assert golomb.decode(codes[8]) == 8
    assert golomb.decode(codes[9]) == 9
    assert golomb.decode(codes[10]) == 10
    assert golomb.decode(codes[11]) == 11
    assert golomb.decode(codes[12]) == 12
    assert golomb.decode(codes[13]) == 13
    assert golomb.decode(codes[14]) == 14
    assert golomb.decode(codes[15]) == 15

    print("Second test finished with success!")

    print("\n------------------------------")
    print("THIRD TEST - ENCODE WITH M = 5")
    print("------------------------------")

    golomb.set_m(5)
    
    codes = ["000", "001", "010", "0110", "0111", "1000", "1001", "1010", "10110", "10111", \
        "11000", "11001", "11010", "110110", "110111", "111000"]

    assert golomb.encode(0) == codes[0]
    assert golomb.encode(1) == codes[1]
    assert golomb.encode(2) == codes[2]
    assert golomb.encode(3) == codes[3]
    assert golomb.encode(4) == codes[4]
    assert golomb.encode(5) == codes[5]
    assert golomb.encode(6) == codes[6]
    assert golomb.encode(7) == codes[7]
    assert golomb.encode(8) == codes[8]
    assert golomb.encode(9) == codes[9]
    assert golomb.encode(10) == codes[10]
    assert golomb.encode(11) == codes[11]
    assert golomb.encode(12) == codes[12]
    assert golomb.encode(13) == codes[13]
    assert golomb.encode(14) == codes[14]
    assert golomb.encode(15) == codes[15]

    print("Third test finished with success!")

    print("\n-------------------------------")
    print("FOURTH TEST - DECODE WITH M = 5")
    print("-------------------------------")

    assert golomb.decode(codes[0]) == 0
    assert golomb.decode(codes[1]) == 1
    assert golomb.decode(codes[2]) == 2
    assert golomb.decode(codes[3]) == 3
    assert golomb.decode(codes[4]) == 4
    assert golomb.decode(codes[5]) == 5
    assert golomb.decode(codes[6]) == 6
    assert golomb.decode(codes[7]) == 7
    assert golomb.decode(codes[8]) == 8
    assert golomb.decode(codes[9]) == 9
    assert golomb.decode(codes[10]) == 10
    assert golomb.decode(codes[11]) == 11
    assert golomb.decode(codes[12]) == 12
    assert golomb.decode(codes[13]) == 13
    assert golomb.decode(codes[14]) == 14
    assert golomb.decode(codes[15]) == 15

    print("Fourth test finished with success!")