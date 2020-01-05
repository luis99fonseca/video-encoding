#include <stdio.h>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <chrono>
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
            for(int i = 0; i < matrix.size(); i++) {
                this->original_matrix.push_back(matrix.at(i));
                
            }
        }

        void encode(Frame* frame, Predictor* predictor, BitStream* bitstream, Golomb* golomb) {
            
            int height = frame->getHeight(), width = frame->getWidth();

            int firstValue = this->original_matrix.at(0) - predictor->predict(0,0,0);
            this->encoded_matrix.push_back(firstValue);
            
            for(int col = 1; col < width; col++)
            {
                int value = (int)(this->original_matrix.at(col) - predictor->predict(this->original_matrix.at(col-1), 0, 0));
                this->encoded_matrix.push_back(value);
            }
            
            for(int line = 1; line < height; line++)
            {
                for (int col = 0; col < width; col++)
                {   
                    int value;
                    if(col == 0)
                    {
                        value = (int)(this->original_matrix.at(line*width + 0) - predictor->predict(0, this->original_matrix.at((line-1)*width + 0), 0));
                    }
                    else 
                    {   
                        int a = this->original_matrix.at(line*width + (col - 1));
                        int b = this->original_matrix.at((line-1)*width + col);
                        int c = this->original_matrix.at((line-1)*width+ (col - 1));
                        value = (int)(this->original_matrix.at(line*width + col) - predictor->predict(a,b,c));
                    }
                    this->encoded_matrix.push_back(value);
                }
            }

            for(int line = 0; line < height; line++)
            {
                for(int col = 0; col < width; col++)
                {
                    vector<int> code = golomb->encode(this->encoded_matrix.at(line*width + col));
                }
            }
        } 
};

int main() {
    IntraFrameEncoder ife;
    Frame444* frame = new Frame444(720, 1280, "../../../python/media/park_joy_444_720p50.y4m");
    JPEG1* predictor = new JPEG1();
    BitStream* bitstream = new BitStream("../../out/park_joy_444_720p50.bin", 'w');
    Golomb* golomb = new Golomb(4);

    int total_time = 0;
    int total_frames = 0;
    bool firstFrame = true;

    while(true)
    {
        std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
        bool playing = frame->advance();

        // movie end
        if(!playing)
            break;
        
        vector<int> Y = frame->getY();
        ife.setMatrix(Y);
        if(firstFrame)
        {
            bitstream->writeString("500\t720\t1280");
            firstFrame = false;
        }
            
        ife.encode(frame, predictor, bitstream, golomb);

        vector<int> U = frame->getU();
        ife.setMatrix(U);
        ife.encode(frame, predictor, bitstream, golomb);

        vector<int> V = frame->getV();
        ife.setMatrix(V);
        ife.encode(frame, predictor, bitstream, golomb);
        
        total_frames++;
        std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
        std::cout << "Frame compressed in " << std::chrono::duration_cast<chrono::seconds>(end - begin).count() << " s;\n";
        break;
    }

    return 0;
}