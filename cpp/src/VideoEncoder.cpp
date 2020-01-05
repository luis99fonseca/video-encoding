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
#include "Encoders.cpp"

int main() {
    IntraFrameEncoder ife;
    Frame444* frame = new Frame444(720, 1280, "../../python/media/park_joy_444_720p50.y4m");
    JPEG1* predictor = new JPEG1();
    BitStream* bitstream = new BitStream("../out/park_joy_444_720p50.bin", 'w');
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
        
        // Com este break, só um frame é codificado
        // break;
    }

    return 0;
}