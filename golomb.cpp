#include <assert.h>
#include <iostream>
#include <cstring>
#include <cmath>
#include <vector>
#include<algorithm>

using namespace std;

class Golomb
{
public:
    double m;
    bool isBase2;

    Golomb(double m)
    {
        assert(m > 0);

        this->m = m;
        this->isBase2 = log2(this->m) == (int)log2(this->m) ? true : false;
    }

    void set_m(double m)
    {
        assert(m > 0);

        this->m = m;
        this->isBase2 = log2(this->m) == (int)log2(this->m) ? true : false;
    }

    vector<int> encode(int n)
    {
        assert(n >= 0);

        return this->isBase2 ? this->base2encoder(n) : this->truncated_encoder(n);
    }

    vector<int> base2encoder(int n)
    {
        int q = floor(n / this->m);
        int r = n % (int)this->m;

        vector<int> unary_code = this->unary_code(q);
        vector<int> binary_code = this->binary_code(r, 1);

        // golomb code
        unary_code.insert(unary_code.end(), binary_code.begin(), binary_code.end());

        return unary_code;
    }

    vector<int> truncated_encoder(int n)
    {
        int b = ceil(log2(this->m));

        int q = floor(n / this->m);
        int r = n % (int)this->m;

        vector<int> unary_code = this->unary_code(q);

        int first_values = pow(2, b) - this->m;

        vector<int> binary_code = r < first_values ? this->binary_code(r, b-1) : this->binary_code(r + pow(2, b) - this->m, b);

        // golomb code
        unary_code.insert(unary_code.end(), binary_code.begin(), binary_code.end());

        return unary_code;
    }

    vector<int> unary_code(int q)
    {
        vector<int> unary_code;
        for (int i = 0; i < q; i++)
        {
            unary_code.push_back(1);
        }
        unary_code.push_back(0);
        return unary_code;
    }

    // TODO: check c++ native function
    vector<int> binary_code(int decimal, int bits)
    {
        vector<int> binary;
        int n = decimal;

        while (true)
        {
            int q = floor(n / 2);
            int bit = n % 2;
            binary.push_back(bit);
            n = q;
            
            if(q == 0) break;
        }

        while (binary.size() < bits)
            binary.push_back(0);
        

        reverse(binary.begin(), binary.end());

        return binary;
    }
};

// main() is where program execution begins.
int main()
{
    Golomb golomb(5);

    vector<int> codes;
    for(int i = 0; i < 15; i++) {
        vector<int> code = golomb.encode(i);
        codes.insert(codes.end(), code.begin(), code.end());
    }
    

    for(int i = 0; i < codes.size(); i++)
        cout << codes.at(i) << ";";
}