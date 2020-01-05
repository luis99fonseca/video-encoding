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
    Golomb()
    {
        this->m = 4; // default value
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

    /**
         * This method updates the value of 'M'.
         * 
         * @param m: new M
         */
    void set_m(double m)
    {
        assert(m > 0);

        this->m = m;
        this->isBase2 = log2(this->m) == (int)log2(this->m) ? true : false;
    }

    /**
         * Get the value of 'M'.
         */
    int get_m() { return this->m; }

    vector<int> encode(int n)
    {
        return this->isBase2 ? this->base2encoder(n) : this->truncated_encoder(n);
    }

    /**
         * This method encodes a given integer 'n' with Golomb encoding, using a power of two value of 'M'.
         * 
         * @param n: integer to encode
         */
    vector<int> base2encoder(int n)
    {

        //check 'n' sign (0 - positive, 1 - negative)
        vector<int> golomb_code;
        golomb_code.push_back(0);
        if (n < 0)
        {
            n = abs(n);
            golomb_code.at(0) = 1;
        }

        // computes values of 'q' and 'r'
        int q = floor(n / this->m);
        int r = n % (int)this->m;

        // computes unary and binary codes of 'q' and 'r', respectively.
        vector<int> unary_code = this->unary_code(q);
        vector<int> binary_code = this->binary_code(r, 2);

        golomb_code.insert(golomb_code.end(), unary_code.begin(), unary_code.end());
        golomb_code.insert(golomb_code.end(), binary_code.begin(), binary_code.end());

        return golomb_code;
    }

    /**
         * This method encodes a given integer 'n' with truncated Golomb encoding.
         * 
         * @param n: integer to encode
         */
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

    /*
        * This method, depending on the value of M, calls the respective method to decode a given list of bits.
        * If M is a power of two, it calls the base2decoder() method. Else, it calls the truncated_decoder() method.
        * 
        * @param bitstream: list of bits to decode
        */
    int decode(vector<int> bitstream)
    {
        assert(bitstream.size() > 0);
        return this->isBase2 ? this->base2decoder(bitstream) : this->truncated_decoder(bitstream);
    }

    /**
         * This method decodes a bitstream with multiple integers.
         * Example: stream_decoder([0,0,0,1,0,0,1,0,0,0,0,0]) -> [1,2,0]
         * 
         * @param bitstream: a list of bits 
        */

    vector<int> stream_decoder(vector<int> bitstream, int total = 0)
    {
        int bit = 0;

        // all decoded integers
        vector<int> decoded;

        if (bitstream.size() == 0)
            return decoded;

        // loop until all bits are decoded
        while (true)
        {
            try
            {
                int sign = bitstream.at(bit);
                bit++;
                vector<int> golomb_code = {sign};
                if (bitstream.at(bit) == 0)
                {
                    golomb_code.push_back(bitstream.at(bit)); // unary_code
                    bit++;
                    for (int i = bit; i < bit + ceil(sqrt(this->m)); i++)
                        golomb_code.push_back(bitstream.at(i));

                    bit += ceil(sqrt(this->m));
                    int decimal = this->decode(golomb_code);
                    decoded.push_back(decimal);
                }
                else
                {
                    while (true)
                    {
                        int unary_bit = bitstream.at(bit);
                        golomb_code.push_back(unary_bit);
                        bit++;
                        if (unary_bit == 0)
                            break;
                    }
                    for (int i = bit; i < bit + ceil(sqrt(this->m)); i++)
                        golomb_code.push_back(bitstream.at(i));

                    bit += ceil(sqrt(this->m));
                    int decimal = this->decode(golomb_code);
                    decoded.push_back(decimal);
                }

                if (bitstream.size() <= bit || decoded.size() == total)
                    break;
            }
            catch (...)
            {
                vector<int> eof = {0};
                return eof;
            }
        }
        return decoded;
    }

    /**
         * This method decodes a given list of bits, encoded with Golomb encoding.
         * 
         * @param bitstream: list of bits to decode
        */
    int base2decoder(vector<int> bitstream)
    {
        int bit = 0;
        bool negative = bitstream.at(bit) == 1;
        bit++;

        int q, r;
        if (bitstream.at(bit) == 0)
        {
            q = 0;
            vector<int> aux;
            for (int i = bit; i < bitstream.size(); i++)
                aux.push_back(bitstream.at(i));
            r = this->binary_to_decimal(aux);
        }
        else
        {
            int i = bit;
            while (bitstream.at(i) == 1)
                i++;
            i--;
            vector<int> binary_code;
            for (int j = i + 1; j < bitstream.size(); j++)
                binary_code.push_back(bitstream.at(j));
            q = i;
            r = this->binary_to_decimal(binary_code);
        }

        return negative ? -1 * (r + q * this->m) : r + q * this->m;
    }

    /**
         * This method decodes a given list of bits, encoded with truncated Golomb encoding.
         * 
         * @param bitstream: list of bits to decode
        */
    int truncated_decoder(vector<int> bitstream)
    {
        int b = ceil(log2(this->m));
        int q, r;
        vector<int> binary_code;
        if (bitstream.at(0) == 0)
        {
            q = 0;
            for (int i = 1; i < bitstream.size(); i++)
                binary_code.push_back(bitstream.at(i));
        }
        else
        {
            int i = 0;
            while (bitstream.at(i) == 1)
                i++;

            q = i;
            for (int j = i; j < bitstream.size(); j++)
                binary_code.push_back(bitstream.at(j));
        }
        int first_values = pow(2, b) - this->m;
        int decimal = this->binary_to_decimal(binary_code);
        return decimal < first_values ? decimal + q * this->m : decimal + this->m - pow(2, b) + q * this->m;
    }

    /**
         * This method, given a binary number, converts it into a natural number. 
        */
    int binary_to_decimal(vector<int> bitstream)
    {
        int decimal = 0;
        for (int i = 0; i < bitstream.size(); i++)
            decimal += bitstream.at(i) * pow(2, bitstream.size() - 1 - i);

        return decimal;
    }

    /**
         * This method, given an integer 'q', convert it into unary code of 1's followed by one 0. 
        */
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

    /**
         * This method, given a natural number, converts it into base2 with a given number of bits.
         * 
         * @param decimal: natural number
         * @param bits: number of bits
         */
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
