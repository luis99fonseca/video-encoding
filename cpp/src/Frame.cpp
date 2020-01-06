#include <stdio.h>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
//#include <opencv2/opencv.hpp>

//using namespace cv;

/**
 * Abstract class representing a Frame. 
 */
class Frame
{
private:
    int height, width;
    std::vector<int> Y, U, V;

public:
    std::fstream file;
    /**
     * Frame constructor.
     * 
     * @param height: frame height
     * @param width: frame width
     * @param fname: video file name.
     */
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

    /**
     * Advances and consumes the current bunch of data, so that it can refresh the current set of matrices with new ones.
     * 
     * @return whether or not the reading (and setting operation was successful)
     */
    bool advance()
    {
        return true;
    }

    /**
     * Height getter.
    */
    int getHeight()
    {
        return this->height;
    }

    /**
     * Width getter.
    */
    int getWidth()
    {
        return this->width;
    }

    /**
     * Y component of frame setter.
     * 
     * @param matrix: matrix of integers.
     */
    void setY(std::vector<int> matrix)
    {
        this->Y = matrix;
    }

    /**
     * U component of frame setter.
     * 
     * @param matrix: matrix of integers.
     */
    void setU(std::vector<int> matrix)
    {
        this->U = matrix;
    }

    /**
     * V component of frame setter.
     * 
     * @param matrix: matrix of integers.
     */
    void setV(std::vector<int> matrix)
    {
        this->V = matrix;
    }

    /**
     * Y component getter. 
    */
    std::vector<int> getY()
    {
        return this->Y;
    }

    /**
     * U component getter. 
    */
    std::vector<int> getU()
    {
        return this->U;
    }

    /**
     * V component getter. 
    */
    std::vector<int> getV()
    {
        return this->V;
    }
};

/**
 * This class, derived from 'Frame', implements a 4:4:4 frame.
 */ 
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
        }
        catch(...)
        {
            Frame::file.close();
            return false;
        }
    }

    int getHeight()
    {
        return Frame::getHeight();
    }

    int getWidth()
    {
        return Frame::getWidth();
    }

    void setY(std::vector<int> matrix)
    {
        Frame::setY(matrix);
    }

    void setU(std::vector<int> matrix)
    {
        Frame::setU(matrix);
    }

    void setV(std::vector<int> matrix)
    {
        Frame::setV(matrix);
    }

    std::vector<int> getY()
    {
        return Frame::getY();
    }

    std::vector<int> getU()
    {
        return Frame::getU();
    }

    std::vector<int> getV()
    {
        return Frame::getV();
    }
};

/**
 * This class, derived from 'Frame', implements a 4:2:2 frame.
*/
class Frame422 : public Frame
{
public:
    Frame422(int height, int width, std::string fname) : Frame(height, width, fname)
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
                for (int i = 0; i < height / 2; i++)
                {
                    for (int j = 0; j < width / 2; j++)
                    {
                        char b;
                        Frame::file.read(&b, 1);
                        U.push_back((int)b);
                    }
                }
                Frame::setU(U);

                std::vector<int> V;
                for (int i = 0; i < height / 2; i++)
                {
                    for (int j = 0; j < width / 2; j++)
                    {
                        char b;
                        Frame::file.read(&b, 1);
                        V.push_back((int)b);
                    }
                }
                Frame::setV(V);
            }

            return true;
        }
        catch(...)
        {
            Frame::file.close();
            return false;
        }
    }

    int getHeight()
    {
        return Frame::getHeight();
    }

    int getWidth()
    {
        return Frame::getWidth();
    }

    void setY(std::vector<int> matrix)
    {
        Frame::setY(matrix);
    }

    void setU(std::vector<int> matrix)
    {
        Frame::setU(matrix);
    }

    void setV(std::vector<int> matrix)
    {
        Frame::setV(matrix);
    }

    std::vector<int> getY()
    {
        return Frame::getY();
    }

    std::vector<int> getU()
    {
        return Frame::getU();
    }

    std::vector<int> getV()
    {
        return Frame::getV();
    }
};

/**
 * This class, derived from 'Frame', implements a 4:2:0 frame.
*/
class Frame420 : public Frame
{
public:
    Frame420(int height, int width, std::string fname) : Frame(height, width, fname)
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
                for (int i = 0; i < height / 4; i++)
                {
                    for (int j = 0; j < width / 4; j++)
                    {
                        char b;
                        Frame::file.read(&b, 1);
                        U.push_back((int)b);
                    }
                }
                Frame::setU(U);

                std::vector<int> V;
                for (int i = 0; i < height / 4; i++)
                {
                    for (int j = 0; j < width / 4; j++)
                    {
                        char b;
                        Frame::file.read(&b, 1);
                        V.push_back((int)b);
                    }
                }
                Frame::setV(V);
            }

            return true;
        }
        catch(...)
        {
            Frame::file.close();
            return false;
        }
    }

    int getHeight()
    {
        return Frame::getHeight();
    }

    int getWidth()
    {
        return Frame::getWidth();
    }

    void setY(std::vector<int> matrix)
    {
        Frame::setY(matrix);
    }

    void setU(std::vector<int> matrix)
    {
        Frame::setU(matrix);
    }

    void setV(std::vector<int> matrix)
    {
        Frame::setV(matrix);
    }

    std::vector<int> getY()
    {
        return Frame::getY();
    }

    std::vector<int> getU()
    {
        return Frame::getU();
    }

    std::vector<int> getV()
    {
        return Frame::getV();
    }
};
