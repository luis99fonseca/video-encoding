#include <stdio.h>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <opencv2/opencv.hpp>


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