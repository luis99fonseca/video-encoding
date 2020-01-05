#include <iostream>
#include <vector>
#include <assert.h>
#include "Golomb.cpp"

using namespace std;

bool unit_encode_test(Golomb golomb, int n, vector<int> output)
{
    vector<int> encoded = golomb.encode(n);

    for (int i = 0; i < encoded.size(); i++)
        assert(encoded.at(i) == output.at(i));

    return true;
}

bool unit_decode_test(Golomb golomb, vector<int> code, int output)
{
    int n = golomb.decode(code);
    assert(n == output);
    return true;
}

int main()
{
    Golomb golomb(4);

    cout << ("------------------------------") << "\n";
    cout << ("FIRST TEST - ENCODE WITH M = 4") << "\n";
    cout << ("------------------------------") << "\n";

    vector<vector<int>> codes = { {0, 0, 0, 0},
                                  {0, 0, 0, 1},
                                  {0, 0, 1, 0},
                                  {0, 0, 1, 1},
                                  {0, 1, 0, 0, 0},
                                  {0, 1, 0, 0, 1},
                                  {0, 1, 0, 1, 0},
                                  {0, 1, 0, 1, 1},
                                  {0, 1, 1, 0, 0, 0},
                                  {0, 1, 1, 0, 0, 1},
                                  {0, 1, 1, 0, 1, 0},
                                  {0, 1, 1, 0, 1, 1},
                                  {0, 1, 1, 1, 0, 0, 0},
                                  {0, 1, 1, 1, 0, 0, 1},
                                  {0, 1, 1, 1, 0, 1, 0},
                                  {0, 1, 1, 1, 0, 1, 1} }; 
    
    for (int code = 0; code < codes.size(); code++)
        unit_encode_test(golomb, code, codes.at(code));

    
    cout << ("------------------------------") << "\n";
    cout << ("SECOND TEST - DECODE WITH M = 4") << "\n";
    cout << ("------------------------------") << "\n";


    for(int code = 0; code < codes.size(); code++)
        unit_decode_test(golomb, codes.at(code), code);


    cout << ("------------------------------") << "\n";
    cout << ("THIRD TEST - DECODE STREAM WITH M = 4") << "\n";
    cout << ("------------------------------") << "\n";
    vector<int> stream = {0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1};
    vector<int> decoded = golomb.stream_decoder(stream, 16);
    
    cout << ("------------------------------") << "\n";
    cout << ("FOURTH TEST - ENCODE WITH M = 5") << "\n";
    cout << ("------------------------------") << "\n";

    golomb.set_m(5);

    vector<vector<int>> codes2 = { 
        {0,0,0}, 
        {0,0,1}, 
        {0,1,0}, 
        {0,1,1,0}, 
        {0,1,1,1}, 
        {1,0,0,0}, 
        {1,0,0,1}, 
        {1,0,1,0}, 
        {1,0,1,1,0}, 
        {1,0,1,1,1},
        {1,1,0,0,0},
        {1,1,0,0,1},
        {1,1,0,1,0},
        {1,1,0,1,1,0},
        {1,1,0,1,1,1},
        {1,1,1,0,0,0}
    };


    for(int code = 0; code < codes2.size(); code++) 
        unit_encode_test(golomb,code,codes2.at(code));

    cout << ("------------------------------") << "\n";
    cout << ("FIFTH TEST - DECODE WITH M = 5") << "\n";
    cout << ("------------------------------") << "\n";

    for(int code = 0; code < codes2.size(); code++) 
        unit_decode_test(golomb,codes2.at(code),code);
    
    
}