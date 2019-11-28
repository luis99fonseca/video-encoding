//file management
#include <iostream>
#include <fstream>
#include <vector>
#include <bitset>
#include <math.h> 

using namespace std;

class BitStream {
    public:
        string fileName;
        fstream fileF;
        streampos filePointer;

        unsigned char read_byte;
        int read_byte_idx;
        bool read_eof;


        BitStream(string fileN){
            fileName = fileN;
            filePointer = 0;

            read_byte_idx = -1;
            read_eof = false;
        };

        vector<bool> readBit(int no){
            vector<bool> bit_list;
            if (read_eof){
                cout << "[DEBUG] EOF Reached!! Cannot read any further.\n";
                return bit_list;
            }

            unsigned char temp_bit;
            for (int i = 0; i < no; i++){
                temp_bit = 0;
                if (read_byte_idx == -1){
                    read_byte_idx = 7;

                    cout << "[DEBUG] Reading again!! \n";

                    fileF.open(fileName, ios::in | ios::binary);
                    fileF.seekg(filePointer);
                    fileF.read(reinterpret_cast<char *>(&read_byte), 1);
                    if (fileF.eof()){
                        cout << "[DEBUG] EOF Reached!! Cannot read any further.\n";
                        fileF.close();
                        break;
                    } else {
                        printf("[DEBUG] has beeng read %u, aka ", (unsigned char) read_byte);
                        cout << bitset<8>(read_byte) << "\n";      // can be removed in the future, here for debuggind porpuses
                        cout << "[DEBUG] tell: " << fileF.tellg() << "\n";
                        filePointer = fileF.tellg();
                        fileF.close();
                    }
                }
                temp_bit |= (read_byte >> read_byte_idx--) & 1;
                cout << "temp_bit é " << temp_bit << "\n"; 
                bit_list.push_back(temp_bit);
            }
            return bit_list;
        }
};

int main(){

 /*    fstream file01;
    file01.open("teste01.txt", ios::out | ios::binary);
    cout << "eyah\n";
    unsigned char temp_byte = 98;
    file01.write(reinterpret_cast<char *>(&temp_byte), 1);

    temp_byte = 1;
    file01.write(reinterpret_cast<char *>(&temp_byte), 1);

    temp_byte = 120;
    file01.write(reinterpret_cast<char *>(&temp_byte), 1);

    file01.close();

    fstream file02; */

    /* reinterpret_cast only guarantees that if you cast a pointer to a different type, and 
    then reinterpret_cast it back to the original type, you get the original value. So in the following:
     */

   /*  char *temp_byte2;
    file02.read(temp_byte2, 1); */
    // pk é que isto nao da caralho?
/* 
    unsigned char temp_byte2;
    
    int n = 8;
    int read_byte_idx = -1;
    unsigned char temp_bit;
    streampos filePointer = 0;
    vector<bool> bit_list;

    for (int i = 0; i < n; i++){
        temp_bit = 0;
        if (read_byte_idx == -1){
            read_byte_idx = 7;

            cout << "[DEBUG] Reading again!! \n";

            file02.open("teste01.txt", ios::in | ios::binary);
            file02.seekg(filePointer);
            file02.read(reinterpret_cast<char *>(&temp_byte2), 1);
            
            if (file02.eof()){
                cout << "[DEBUG] EOF Reached!! Cannot read any further.\n";
                file02.close();
                break;
            } else {
                printf("[DEBUG] has beeng read %u, aka ", (unsigned char) temp_byte2);
                cout << bitset<8>(temp_byte2) << "\n";      // can be removed in the future, here for debuggind porpuses
                cout << "[DEBUG] tell: " << file02.tellg() << "\n";
                filePointer = file02.tellg();
                file02.close();
            }
        }
        temp_bit |= (temp_byte2 >> read_byte_idx--) & 1;
        cout << "temp_bit é " << temp_bit; 
        bit_list.push_back(temp_bit);
        
    } */

   /*  BitStream bs("test01.txt");
    vector<bool> bit_list = bs.readBit(8);    

    cout << "Output of begin and end: ["; 
    for (auto i = bit_list.begin(); i != bit_list.end(); ++i) 
        cout << *i << ", "; 
    cout << "]\n";
    
    bit_list = bs.readBit(4);    

    cout << "Output of begin and end: ["; 
    for (auto i = bit_list.begin(); i != bit_list.end(); ++i) 
        cout << *i << ", "; 
    cout << "]\n"; */
    
    /*
    vector<bool> vecOfNums2{ 0,1,1,0,0,0,1,0 };
    if (vecOfNums2 == bit_list){
        cout << "[WARNING] IGUAIS!!\n";
    }
     */

    cout << (int) log2(8)+1 << "\n";
    return 0;
}

