#include "BitStream.cpp"
#include <assert.h>     /* assert */



int main(){


    bool test01 = false;
    bool test02 = true;
    
    // ---------------READING TESTING--------------
    if (test01){

        BitStream bitstream01("test01.txt");
        vector <bool> vecReading;

        vecReading = { 1, 1, 0, 0, 1, 0, 0, 0};
        assert (bitstream01.readBit(8) == vecReading);

        vecReading = {0, 1, 1, 1};
        assert (bitstream01.readBit(4) == vecReading);

        vecReading = { 1, 0, 0, 0};
        assert (bitstream01.readBit(4) == vecReading);

        vecReading = { 0, 1, 1, 0, 0, 0, 1, 1};
        assert (bitstream01.readByte() == vecReading);

        vecReading = {};
        assert (bitstream01.readBit(8) == vecReading);

        vecReading = {};
        assert (bitstream01.readBit(4) == vecReading);
    }

    // ---------------WRITING TESTING--------------
    if (test02){

        BitStream bitstream02("test02.txt");
        assert (!bitstream02.writeBit(256, 1));
        assert (!bitstream02.writeBit(3,1));

        bitstream02.writeBit(3, 2);
        bitstream02.writeBit(1, 2);
        bitstream02.writeBit(4, 4);
        bitstream02.writeByte(1);
        bitstream02.writeBit(1, 1);
        bitstream02.writeBit(1, 3);
        bitstream02.writeBit(1, 4);

        bitstream02.writeBit(1, 15);
        bitstream02.writeBit(1, 1);
        

        BitStream bitstream022("test02.txt");
        vector <bool> vecReading;

        vecReading = {1, 1, 0, 1, 0, 1, 0, 0};
        assert (bitstream022.readBit(8) == vecReading);

        vecReading = {0, 0, 0, 0, 0, 0, 0, 1};
        assert (bitstream022.readBit(8) == vecReading);

        vecReading = {1, 0, 0, 1, 0, 0, 0, 1};
        assert (bitstream022.readBit(8) == vecReading); 

        vecReading = {0, 0, 0, 0, 0, 0, 0, 0};
        assert (bitstream022.readBit(8) == vecReading); 

        vecReading = {0, 0, 0, 0, 0, 0, 1, 1};
        assert (bitstream022.readBit(8) == vecReading); 


    }

    return 0;
}
