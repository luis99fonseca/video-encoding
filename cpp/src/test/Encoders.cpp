#include <stdio.h>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <opencv2/opencv.hpp>
#include "Frame.cpp"
#include "BitStream.cpp"
#include "Golomb.cpp"
#include "Predictor.cpp"


using namespace cv;

class IntraFrameEncoder
{
    private:
        std::vector<int> original_matrix;
        std::vector<int> encoded_matrix;

    public:
        IntraFrameEncoder() {

        }

        void writeCode(std::vector<int> code){};

        void setMatrix(std::vector<int> matrix)
        {
            this->original_matrix = matrix;
        }

        void encode(Frame frame, BitStream bitstream, Predictor predictor) {// TODO: depois alterar o predictor

            int firstValue = (int)(this->original_matrix.at(0) - predictor.predict(0,0,0));
            this->encoded_matrix.push_back(firstValue);
        } 
};

int main() {
    IntraFrameEncoder ife;
    Frame444 frame(720, 1280, "../../../python/media/park_joy_444_720p50.y4m");
    frame.advance();

    return 0;
}