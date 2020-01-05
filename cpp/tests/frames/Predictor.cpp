
#include <iostream>

using namespace std;

class Predictor {
    public: 
        virtual int predict(unsigned char a, unsigned char b, unsigned char c) = 0;
};

class JPEG1 : public Predictor {
    public:
        int predict(unsigned char a, unsigned char b, unsigned char c){
            return a;
        };
};

class JPEG2 : public Predictor {
    public:
        int predict(unsigned char a, unsigned char b, unsigned char c){
            return b;
        };
};

class JPEG3 : public Predictor {
    public:
        int predict(unsigned char a, unsigned char b, unsigned char c){
            return c;
        };
};

class JPEG4 : public Predictor {
    public:
        int predict(unsigned char a, unsigned char b, unsigned char c){
            return a + b - c;
        };
};

class JPEG5 : public Predictor {
    public:
        int predict(unsigned char a, unsigned char b, unsigned char c){
            return a + ((b - c) / 2);
        };
};

class JPEG6 : public Predictor {
    public:
        int predict(unsigned char a, unsigned char b, unsigned char c){
            return b + ((a - c) / 2);
        };
};

class JPEG7 : public Predictor {
    public:
        int predict(unsigned char a, unsigned char b, unsigned char c){
            return (a + b) / 2;
        };
};

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

int main(){
    Predictor* pred01;
    pred01 = new JPEG1();
    
    cout << pred01->predict(10, 10, 10) << "\n";

    cout << 5 / 2 << "\n";

    pred01 = new JPEGLS();

    cout << "> " << pred01->predict(5,10,3) << "\n";

    return 0;
}