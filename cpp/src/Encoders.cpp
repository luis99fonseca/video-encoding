#include <stdio.h>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <chrono>
//#include <opencv2/opencv.hpp>


//using namespace cv;

/**
 * This class implements a lossless intra-frame encoder, using 7PEG linear predictors.
 */
class IntraFrameEncoder
{
    private:
        std::vector<int> original_matrix;
        std::vector<int> encoded_matrix;

    public:
        /**
         * Default constructor.
         */
        IntraFrameEncoder() {}

        /**
         * This method writes a list of bits on file, using the Bitstream class.
         * 
         * @param code: list with bits to encode. 
        */
        void writeCode(std::vector<int> code){};

        /**
         * This method sets current matrix of the encoder to 'new_matrix'.
         * 
         * @param new_matrix: new matrix of type Y, U or V. 
        */
        void setMatrix(std::vector<int> matrix)
        {   
            for(int i = 0; i < matrix.size(); i++) {
                this->original_matrix.push_back(matrix.at(i));
                
            }
        }

        /**
         * This method encodes the original matrix in a new one, based on the current predictor.
         * It also uses golomb codification for the entropy encoding.
         * 
         * @param frame: frame object to encode.
         * @param predictor: predictor object to be used.
         * @param bitstream: bitstream object to write the golomb codes to a file.
         * @param golomb: golomb object for the entropy encoding.
         */
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