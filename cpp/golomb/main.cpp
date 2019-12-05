#include <iostream>
#include <vector>
#include <assert.h>
#include "golomb.cpp"

using namespace std;

bool unit_test(Golomb golomb, int n, vector<int> output)
{
    vector<int> encoded = golomb.encode(n);

    for(int i = 0; i < encoded.size(); i++) 
        assert(encoded.at(i) == output.at(i));
        
    return true;
}


int main()
{   
    Golomb golomb(4);

    cout << ("------------------------------") << "\n";
    cout << ("FIRST TEST - ENCODE WITH M = 4") << "\n";
    cout << ("------------------------------") << "\n";

    vector<vector<int>> codes = { 
        {0,0}, 
        {0,1}, 
        {0,1,0}, 
        {0,1,1}, 
        {1,0,0}, 
        {1,0,1}, 
        {1,0,1,0}, 
        {1,0,1,1}, 
        {1,1,0,0}, 
        {1,1,0,1},
        {1,1,0,1,0},
        {1,1,0,1,1},
        {1,1,1,0,0},
        {1,1,1,0,1},
        {1,1,1,0,1,0},
        {1,1,1,0,1,1}
    };

    for(int code = 0; code < codes.size(); code++) 
        unit_test(golomb,code,codes.at(code));

    cout << ("------------------------------") << "\n";
    cout << ("SECOND TEST - DECODE WITH M = 4") << "\n";
    cout << ("------------------------------") << "\n";

    vector<vector<int>> codes = { 
        {0,0}, 
        {0,1}, 
        {0,1,0}, 
        {0,1,1}, 
        {1,0,0}, 
        {1,0,1}, 
        {1,0,1,0}, 
        {1,0,1,1}, 
        {1,1,0,0}, 
        {1,1,0,1},
        {1,1,0,1,0},
        {1,1,0,1,1},
        {1,1,1,0,0},
        {1,1,1,0,1},
        {1,1,1,0,1,0},
        {1,1,1,0,1,1}
    };
    
    for(int code = 0; code < codes.size(); code++) 
        unit_test(golomb,code,codes.at(code));

}