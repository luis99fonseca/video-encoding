#include <assert.h>
#include <iostream>
#include <cstring>
#include <cmath>
#include <vector>
#include <algorithm>

using namespace std;

/**
 * This class implements the Golomb codification to compress information.
 * It encodes an integer based on a given value of M. 
 * The codification is the result of the concatenation of an unary code with a binary code,
 * given by the quotient and remainder of the division between integer value and M, respectively.
*/
class Golomb
{
    private:
        double m;
        bool isBase2;

    public:

        /**
         * Default constructor. 
         */
        Golomb() {
            this->m = 4;    // default value
            this->isBase2 = true;
        }

        /**
         * Constructor with a given value of 'M'. 
         */
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

        int get_m() { return this->m; }

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

            vector<int> binary_code = r < first_values ? this->binary_code(r, b - 1) : this->binary_code(r + pow(2, b) - this->m, b);

            // golomb code
            unary_code.insert(unary_code.end(), binary_code.begin(), binary_code.end());

            return unary_code;
        }

        int decode(vector<int> bitstream)
        {
            assert(bitstream.size() > 0);
            return this->isBase2 ? this->base2decoder(bitstream) : this->truncated_decoder(bitstream);
        }

        int base2decoder(vector<int> bitstream)
        {
            int q, r;
            if (bitstream.at(0) == 0)
            {
                q = 0;
                vector<int> aux;
                for(int i = 1; i < bitstream.size(); i++) 
                    aux.push_back(bitstream.at(i));
                r = this->binary_to_decimal(aux);
            }
            else
            {
                int i = 0;
                while(bitstream.at(i) == 1) i++;
                vector<int> unary_code, binary_code;
                for(int j = 0; j < i + 1; j++) unary_code.push_back(bitstream.at(j));
                for(int j = i + 1; j < bitstream.size(); j++) binary_code.push_back(bitstream.at(j));

                q = i;
                r = this->binary_to_decimal(binary_code);
            }
            return r + q * this->m;
        }

        int truncated_decoder(vector<int> bitstream)
        {
            int b = ceil(log2(this->m));
            int q, r;
            vector<int> binary_code;
            if (bitstream.at(0) == 0) 
            {
                q = 0;
                for(int i = 1; i < bitstream.size(); i++) 
                    binary_code.push_back(bitstream.at(i));
            }
            else 
            {
                int i = 0;
                while (bitstream.at(i) == 1) i++;

                q = i;
                for(int j = i; j < bitstream.size(); j++) 
                    binary_code.push_back(bitstream.at(j));
            }
            int first_values = pow(2,b) - this->m;
            int decimal = this->binary_to_decimal(binary_code);
            return decimal < first_values ? decimal + q * this->m : decimal + this->m - pow(2,b) + q * this->m;
        }

        int binary_to_decimal(vector<int> bitstream)
        {
            int decimal = 0;
            for (int i = 0; i < bitstream.size(); i++)
                decimal += bitstream.at(i) * pow(2, bitstream.size() - 1 - i);
                
            return decimal;
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

                if (q == 0)
                    break;
            }

            while (binary.size() < bits)
                binary.push_back(0);

            reverse(binary.begin(), binary.end());

            return binary;
        }
};
