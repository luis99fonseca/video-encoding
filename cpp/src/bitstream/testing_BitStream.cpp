#include "BitStream.cpp"
#include <assert.h>     /* assert */



int main(){


    bool test01 = true;
    bool test02 = true;
    bool test03 = true;
    bool test04 = true;
    
    // ---------------READING TESTING--------------
    if (test01){

        BitStream bitstream01("test01.txt", 'r');
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

        bitstream01.closeFile();
    }

    // ---------------WRITING TESTING--------------
    if (test02){

        BitStream bitstream02("test02.txt", 'w');
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

        bitstream02.writeBit(1, 1);
        bitstream02.writeBit(2, 3);
        
        vector <bool> vecReading;

        vecReading = {};
        assert (bitstream02.readBit(4) == vecReading);

        bitstream02.closeFile();

        BitStream bitstream022("test02.txt", 'r');
        
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

        vecReading = {1, 0, 1, 0, 0, 0, 0, 0};
        assert (bitstream022.readBit(8) == vecReading); 

        assert (bitstream022.writeBit(1, 2) == false);

        bitstream022.closeFile();

    }

    // ---------------STRING TESTING--------------
    if (test03){
        BitStream bitstream03("test03.txt", 'w');

        bitstream03.writeString("ola");
        bitstream03.writeString("adeus");
        bitstream03.closeFile();

        BitStream bitstream032("test03.txt", 'r');
        assert (bitstream032.readString() == "ola");
        assert (bitstream032.readString() == "adeus");

    }

    // ---------------WRITING TESTING--------------
    if (test04){
        BitStream bitstream041("test04.txt", 'w');
        vector <int> vecReadingInt;    //nota, aqui estão ints;

        vecReadingInt = {1,0,1,1,1,1,0,1,0,1,1};
        bitstream041.writeArray(vecReadingInt);

        bitstream041.closeFile();

        BitStream bitstream042("test04.txt", 'r');

        vector <bool> vecReadingBool;    //nota, aqui estão ints;

        vecReadingBool = {1,0,1,1,1,1,0,1,0,1,1};
        assert (bitstream042.readBit(vecReadingBool.size()) == vecReadingBool);

    }

    return 0;
}
