cmake_minimum_required(VERSION 2.8)
project( VideoEncoder )
find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )
add_executable( VideoEncoder VideoEncoder.cpp )
target_link_libraries( VideoEncoder ${OpenCV_LIBS} )