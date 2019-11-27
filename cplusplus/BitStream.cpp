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

        unsigned char write_byte;
        int write_byte_idx;
        std::ofstream::openmode write_mode;

        // TODO: nao inicializations se desnecessárias
        BitStream(string fileN){
            fileName = fileN;
            filePointer = 0;

            read_byte_idx = -1;
            read_eof = false;

            write_byte = 0;
            write_byte_idx = 7;

            write_mode = std::ofstream::trunc;

        };

        vector<bool> readBit(int no){
            vector<bool> bit_list{};    // TODO: pode nao ser preciso inicializar, maybe nos testes comparo com NULL
            if (read_eof){
                cout << "[DEBUG] EOF Reached!!! Cannot read any further.\n";
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
                        read_eof = true;
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

        bool writeBit(int number, int no_bits = 8){

            if ((int)log2(number) + 1 > no_bits){
                printf("[ERROR] to convert int {%d} into %d-bits word\n", number, no_bits);
                return false;
            }

           
            for (int idx = no_bits - 1; idx >= 0; idx--) {
                cout << "MODE: " << write_mode << "\n";
                unsigned char temp_bit = (number >> idx) & 1;
                // TODO: tentar simplificar os shifts, so para 1

                write_byte |= (temp_bit << write_byte_idx--);
                
                if (write_byte_idx == -1){
                    fileF.open(fileName, ios::out | ios::binary | write_mode);
                    cout << "[WARNING] Writing: " << bitset<8>(write_byte) << "\n";
                    fileF.write(reinterpret_cast<char *> (&write_byte), 1);
                    fileF.close();
                    write_mode = std::ofstream::app;
                    /* cout << "MODE2: " << write_mode << "\n"; */

                    write_byte_idx = 7;
                    write_byte = 0;
                }
            }
            return true;
        }

        // obsolete
        bool writeBit2(int number, int no_bits = 8){

            if ((int)log2(number) + 1 > no_bits){
                printf("[ERROR] to convert int {%d} into %d-bits word\n", number, no_bits);
                return false;
            }

            int temp_counter = no_bits;
            while (true){
                cout << "MODE: " << write_mode << "\n";
                if (write_byte_idx == -1){
                    fileF.open(fileName, ios::out | ios::binary | write_mode);
                    cout << "[WARNING] Writing: " << bitset<8>(write_byte) << "\n";
                    fileF.write(reinterpret_cast<char *> (&write_byte), 1);
                    fileF.close();
                    write_mode = std::ofstream::app;
                    /* cout << "MODE2: " << write_mode << "\n"; */

                    write_byte_idx = 7;
                    write_byte = 0;
                }
                if (temp_counter <= 0){
                    return true;
                }
                write_byte_idx -= (no_bits % (8 + 1));
                temp_counter -=  (no_bits % (8 + 1));
                cout << "[DEBUG] left: " << write_byte_idx + 1 << "; used: " << 8 - write_byte_idx - 1 << "\n";
                write_byte |= number << (write_byte_idx + 1);
                cout << "[DEBUG] i: " << write_byte_idx << " - " << bitset<8>(write_byte) << " - " << temp_counter << "\n";

            }

        }

        vector<bool> readByte(){
            return readBit(8);
        }

        bool writeByte(int number){
            return writeBit(number, 8);
        }
};