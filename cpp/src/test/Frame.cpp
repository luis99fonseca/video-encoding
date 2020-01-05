#include <stdio.h>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <opencv2/opencv.hpp>

using namespace cv;

class Frame
{
private:
    int height, width;
    std::vector<int> Y, U, V;

public:
    std::fstream file;
    Frame(int height, int width, std::string fname)
    {
        this->height = height;
        this->width = width;
        this->file.open(fname, std::ios::in);
        if (this->file.is_open())
        { //checking whether the file is open
            std::string header;
            getline(this->file, header);
            std::cout << header << "\n";
        }
    }

    bool advance()
    {
        return true;
    }

    int getHeight()
    {
        return this->height;
    }

    int getWidth()
    {
        return this->width;
    }

    void setY(std::vector<int> matrix)
    {
        this->Y = matrix;
    }

    void setU(std::vector<int> matrix)
    {
        this->U = matrix;
    }

    void setV(std::vector<int> matrix)
    {
        this->V = matrix;
    }

    std::vector<int> getY()
    {
        return this->Y;
    }

    std::vector<int> getU()
    {
        return this->U;
    }

    std::vector<int> getV()
    {
        return this->V;
    }
};

class Frame444 : public Frame
{
public:
    Frame444(int height, int width, std::string fname) : Frame(height, width, fname)
    {
    }

    bool advance()
    {
        try
        {
            if (Frame::file.is_open())
            { //checking whether the file is open
                std::string frameWord;
                getline(Frame::file, frameWord);
                std::cout << frameWord << "\n";

                int height = Frame::getHeight(), width = Frame::getWidth();

                std::vector<int> Y;
                for (int i = 0; i < height; i++)
                {
                    for (int j = 0; j < width; j++)
                    {
                        char b;
                        Frame::file.read(&b, 1);
                        Y.push_back((int)b);
                    }
                }
                Frame::setY(Y);

                std::vector<int> U;
                for (int i = 0; i < height; i++)
                {
                    for (int j = 0; j < width; j++)
                    {
                        char b;
                        Frame::file.read(&b, 1);
                        U.push_back((int)b);
                    }
                }
                Frame::setU(U);

                std::vector<int> V;
                for (int i = 0; i < height; i++)
                {
                    for (int j = 0; j < width; j++)
                    {
                        char b;
                        Frame::file.read(&b, 1);
                        V.push_back((int)b);
                    }
                }
                Frame::setV(V);
            }

            return true;
        }catch(...)
        {
            Frame::file.close();
            return false;
        }
    }
};
