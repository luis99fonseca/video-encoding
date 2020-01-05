//file management
#include <iostream>
#include <fstream>
#include <vector>
#include <bitset>
#include <math.h>
#include <assert.h>     /* assert */
#include <set>
#include <string>

using namespace std;

/**
 * Class optimised to read/write bits from/to a file.
*/
class BitStream {
    public:

        char modeF;
        fstream fileF;
        
        unsigned char read_byte;
        int read_byte_idx;
        bool read_eof;

        unsigned char write_byte;
        int write_byte_idx;

        bool closedF;

        /**
         * Default constructor. 
        */
        BitStream();

        /**
         * Constructor with a given file name and a opening mode.
         * 
         * @param fileN: file name.
         * @param mode: opening mode.
         */
        BitStream(string fileN, char mode){
            
            std::set<char> allowedModes;
            allowedModes.insert('r');
            allowedModes.insert('w');
            assert ((allowedModes.find(mode) != allowedModes.end()));

            // this.file
            modeF = mode;
            modeF == 'r' ? fileF.open(fileN, ios::in | ios::binary) : fileF.open(fileN, ios::out | ios::binary | std::ofstream::trunc);

            read_byte_idx = -1;
            read_eof = false;

            write_byte = 0;
            write_byte_idx = 7;

            closedF = false;

        };

        /**
         * Closes the file, such that no further operations can be done.
         * If there is a incomplete byte to be written, writes it.
         */
        void closeFile(){
            if (write_byte_idx != 7 && modeF == 'w'){
                fileF.write(reinterpret_cast<char *> (&write_byte), 1);
            }
            fileF.close();
        }

        /**
         * This method reads a given number of bits from a file.
         * 
         * @param no: number of bits to read
         * @return: list of bits read
         */
        vector<bool> readBit(int no){
            vector<bool> bit_list{};

            if (modeF == 'w'){
                printf("[ERROR] Class defined of Writing only. Not allowed to Read!\n");
                return bit_list;
            }

            if (read_eof){
                cout << "[DEBUG] EOF Reached!!! Cannot read any further.\n";
                return bit_list;
            }

            if (closedF){
                cout << "[ERROR] Class closed! Can't operate any further!\n";
                return bit_list;
            }

            unsigned char temp_bit;
            for (int i = 0; i < no; i++){
                temp_bit = 0;
                if (read_byte_idx == -1){
                    read_byte_idx = 7;

                    cout << "[DEBUG] Reading again!! \n";

                    fileF.read(reinterpret_cast<char *>(&read_byte), 1);
                    if (fileF.eof()){
                        cout << "[DEBUG] EOF Reached!! Cannot read any further.\n";
                        read_eof = true;
                        fileF.close();
                        break;
                    } else {
                        printf("[DEBUG] has beeng read %u, aka ", (unsigned char) read_byte);
                        cout << bitset<8>(read_byte) << "\n";    
                    }
                }
                temp_bit |= (read_byte >> read_byte_idx--) & 1;
                cout << "temp_bit é " << temp_bit << "\n"; 
                bit_list.push_back(temp_bit);
            }
            return bit_list;
        }

        /**
         * This method writes a given number of bits to a file.
         * 
         * :@param number: number to write in the file
         * :@param no_bits: number fo bits to be written into 
         */
        bool writeBit(int number, int no_bits = 8){

            if (modeF == 'r'){
                printf("[ERROR] Class defined of Reading only. Not allowed to Write!\n");
                return false;
            }

            if ((int)log2(number) + 1 > no_bits){
                printf("[ERROR] to convert int {%d} into %d-bits word\n", number, no_bits);
                return false;
            }

            if (closedF){
                cout << "[ERROR] Class closed! Can't operate any further!\n";
                return false;
            }

            for (int idx = no_bits - 1; idx >= 0; idx--) {
                unsigned char temp_bit = (number >> idx) & 1;

                write_byte |= (temp_bit << write_byte_idx--);
                
                if (write_byte_idx == -1){
                    cout << "[WARNING] Writing: " << bitset<8>(write_byte) << "\n";
                    fileF.write(reinterpret_cast<char *> (&write_byte), 1);
                    /* cout << "MODE2: " << write_mode << "\n"; */
                    write_byte_idx = 7;
                    write_byte = 0;
                }
            }
            return true;
        }

        /**
         * :@param array: array of numbers to write in the file
         * :@param no_bits: number fo bits to be written into
         * :@return
         */
        bool writeArray(vector<int> array){

            int no_bits = 1;
            if (modeF == 'r'){
                printf("[ERROR] Class defined of Reading only. Not allowed to Write!\n");
                return false;
            }

            if (closedF){
                cout << "[ERROR] Class closed! Can't operate any further!\n";
                return false;
            }

            for (auto &number : array) // access by reference to avoid copying
            {  
                if ((int)log2(number) + 1 > no_bits){
                    printf("[ERROR] to convert int {%d} into %d-bits word\n", number, no_bits);
                    return false;   
                }
                for (int idx = no_bits - 1; idx >= 0; idx--) {
                    unsigned char temp_bit = (number >> idx) & 1;

                    write_byte |= (temp_bit << write_byte_idx--);
                    
                    if (write_byte_idx == -1){
                        cout << "[WARNING] Writing: " << bitset<8>(write_byte) << "\n";
                        fileF.write(reinterpret_cast<char *> (&write_byte), 1);
                        /* cout << "MODE2: " << write_mode << "\n"; */
                        write_byte_idx = 7;
                        write_byte = 0;
                    }
                }
            }

            
            return true;
        }

        /**
         * Writes an entire line enoded in utf-8 format; Line breaker is appended.
         * 
         * :@param message: String to write
         * :@return Whether or not the writing was successful
        */
        bool writeString(string message){
            try {
                fileF << message << "\n";
                return true;
            } catch (int e){
                return false;
            }
        }

        /**
         * Reads and returns an entire line decoded in utf-8 format.
         */
        string readString(){
            string temp_string;
            getline(fileF, temp_string);
            return temp_string;
        }

        /**
         * Reads one byte from a file. 
         */
        vector<bool> readByte(){
            return readBit(8);
        }

        /**
         * Writes one byto to a file. 
         */
        bool writeByte(int number){
            return writeBit(number, 8);
        }
};