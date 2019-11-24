//file management
#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

class BitStream {
    public:
        string fileName;
        int *filePointer;

        int read_byte;
        int read_byte_idx;
        bool read_eof = false;


        BitStream(string fileN){
            fileName = fileN;
        };

        vector<bool> readBit(int no){
            vector<bool> res;
            res.push_back(0);
            return res; 
        }
};

int main(){

   /*  cout << "hello world\n" << "adues";

    ofstream myFile("cplusbad.txt");
    myFile << "jesus crhsit";
    myFile.close();

    string myTexto;
    ifstream myFile2("cplusbad.txt");
    while (getline (myFile2, myTexto)) {
        // Output the text from the file
        cout << myTexto << "\n";
    }
    // Close the file
    myFile2.close();

    BitStream ola("tambem");
    cout << ola.fileName << "\n";
    bool vdd = 1;
    cout << vdd;

    vector<bool> temp_v = ola.readBit(1); 
    for (std::vector<bool>::const_iterator i = temp_v.begin(); i != temp_v.end(); ++i){
        std::cout << *i << ' ';
    } */

    fstream file01;
    file01.open("teste01.txt", ios::out | ios::binary);
    cout << "eyah";
    unsigned char temp_byte = 255;
    file01.write(reinterpret_cast<char *>(&temp_byte), 1);

    file01.close();

    fstream file02;

    /* reinterpret_cast only guarantees that if you cast a pointer to a different type, and 
    then reinterpret_cast it back to the original type, you get the original value. So in the following:
     */

    file02.open("teste01.txt", ios::in | ios::binary);

   /*  char *temp_byte2;
    file02.read(temp_byte2, 1); */
    // pk é que isto nao da caralho?

    unsigned char temp_byte2;
    file02.read(reinterpret_cast<char *>(&temp_byte2), 1);
    printf("%u", (unsigned char) temp_byte2);

    file02.close();
    return 0;
}

