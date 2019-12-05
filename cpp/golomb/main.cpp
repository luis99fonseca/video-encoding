#include <iostream>
#include <vector>
#include "golomb.cpp"

using namespace std;
int main()
{   
    Golomb golomb(5);
    
    for(int c = 0; c <= 15; c++) {
        vector<int> code = golomb.encode(c);
        int decimal = golomb.decode(code);
        cout << decimal << "\n";
    }
    

    
}