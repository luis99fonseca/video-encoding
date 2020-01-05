
#include <iostream>

using namespace std;

/**
 * Abstract class predictor;
 */
class Predictor {
    public: 
        virtual int predict(unsigned char a, unsigned char b, unsigned char c) = 0;
};

/**
 * JPEG1 linear predictor.
*/
class JPEG1 : public Predictor {
    public:
        int predict(unsigned char a, unsigned char b, unsigned char c){
            return a;
        };
};

/**
 * JPEG2 linear predictor.
*/
class JPEG2 : public Predictor {
    public:
        int predict(unsigned char a, unsigned char b, unsigned char c){
            return b;
        };
};

/**
 * JPEG3 linear predictor.
*/
class JPEG3 : public Predictor {
    public:
        int predict(unsigned char a, unsigned char b, unsigned char c){
            return c;
        };
};

/**
 * JPEG4 linear predictor.
*/
class JPEG4 : public Predictor {
    public:
        int predict(unsigned char a, unsigned char b, unsigned char c){
            return a + b - c;
        };
};

/**
 * JPEG5 linear predictor.
*/
class JPEG5 : public Predictor {
    public:
        int predict(unsigned char a, unsigned char b, unsigned char c){
            return a + ((b - c) / 2);
        };
};

/**
 * JPEG6 linear predictor.
*/
class JPEG6 : public Predictor {
    public:
        int predict(unsigned char a, unsigned char b, unsigned char c){
            return b + ((a - c) / 2);
        };
};

/**
 * JPEG7 linear predictor.
*/
class JPEG7 : public Predictor {
    public:
        int predict(unsigned char a, unsigned char b, unsigned char c){
            return (a + b) / 2;
        };
};

/**
 * JPEG-LS predictor
 */
class JPEGLS: public Predictor {
    public:
        int predict(unsigned char a, unsigned char b, unsigned char c){
           if (c >= max(a, b)){
               return min(a,b);
           }
           if (c <= min(a,b)){
               return max(a,b);
           }
           return a + b - c;
        };
        
};

