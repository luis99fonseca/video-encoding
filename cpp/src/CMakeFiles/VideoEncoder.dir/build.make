# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/tiagocm/Documents/Code/video-encoding/cpp/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/tiagocm/Documents/Code/video-encoding/cpp/src

# Include any dependencies generated for this target.
include CMakeFiles/VideoEncoder.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/VideoEncoder.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/VideoEncoder.dir/flags.make

CMakeFiles/VideoEncoder.dir/VideoEncoder.cpp.o: CMakeFiles/VideoEncoder.dir/flags.make
CMakeFiles/VideoEncoder.dir/VideoEncoder.cpp.o: VideoEncoder.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/tiagocm/Documents/Code/video-encoding/cpp/src/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/VideoEncoder.dir/VideoEncoder.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/VideoEncoder.dir/VideoEncoder.cpp.o -c /home/tiagocm/Documents/Code/video-encoding/cpp/src/VideoEncoder.cpp

CMakeFiles/VideoEncoder.dir/VideoEncoder.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/VideoEncoder.dir/VideoEncoder.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/tiagocm/Documents/Code/video-encoding/cpp/src/VideoEncoder.cpp > CMakeFiles/VideoEncoder.dir/VideoEncoder.cpp.i

CMakeFiles/VideoEncoder.dir/VideoEncoder.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/VideoEncoder.dir/VideoEncoder.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/tiagocm/Documents/Code/video-encoding/cpp/src/VideoEncoder.cpp -o CMakeFiles/VideoEncoder.dir/VideoEncoder.cpp.s

CMakeFiles/VideoEncoder.dir/VideoEncoder.cpp.o.requires:

.PHONY : CMakeFiles/VideoEncoder.dir/VideoEncoder.cpp.o.requires

CMakeFiles/VideoEncoder.dir/VideoEncoder.cpp.o.provides: CMakeFiles/VideoEncoder.dir/VideoEncoder.cpp.o.requires
	$(MAKE) -f CMakeFiles/VideoEncoder.dir/build.make CMakeFiles/VideoEncoder.dir/VideoEncoder.cpp.o.provides.build
.PHONY : CMakeFiles/VideoEncoder.dir/VideoEncoder.cpp.o.provides

CMakeFiles/VideoEncoder.dir/VideoEncoder.cpp.o.provides.build: CMakeFiles/VideoEncoder.dir/VideoEncoder.cpp.o


# Object files for target VideoEncoder
VideoEncoder_OBJECTS = \
"CMakeFiles/VideoEncoder.dir/VideoEncoder.cpp.o"

# External object files for target VideoEncoder
VideoEncoder_EXTERNAL_OBJECTS =

VideoEncoder: CMakeFiles/VideoEncoder.dir/VideoEncoder.cpp.o
VideoEncoder: CMakeFiles/VideoEncoder.dir/build.make
VideoEncoder: /usr/local/lib/libopencv_dnn.so.4.2.0
VideoEncoder: /usr/local/lib/libopencv_gapi.so.4.2.0
VideoEncoder: /usr/local/lib/libopencv_highgui.so.4.2.0
VideoEncoder: /usr/local/lib/libopencv_ml.so.4.2.0
VideoEncoder: /usr/local/lib/libopencv_objdetect.so.4.2.0
VideoEncoder: /usr/local/lib/libopencv_photo.so.4.2.0
VideoEncoder: /usr/local/lib/libopencv_stitching.so.4.2.0
VideoEncoder: /usr/local/lib/libopencv_video.so.4.2.0
VideoEncoder: /usr/local/lib/libopencv_videoio.so.4.2.0
VideoEncoder: /usr/local/lib/libopencv_imgcodecs.so.4.2.0
VideoEncoder: /usr/local/lib/libopencv_calib3d.so.4.2.0
VideoEncoder: /usr/local/lib/libopencv_features2d.so.4.2.0
VideoEncoder: /usr/local/lib/libopencv_flann.so.4.2.0
VideoEncoder: /usr/local/lib/libopencv_imgproc.so.4.2.0
VideoEncoder: /usr/local/lib/libopencv_core.so.4.2.0
VideoEncoder: CMakeFiles/VideoEncoder.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/tiagocm/Documents/Code/video-encoding/cpp/src/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable VideoEncoder"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/VideoEncoder.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/VideoEncoder.dir/build: VideoEncoder

.PHONY : CMakeFiles/VideoEncoder.dir/build

CMakeFiles/VideoEncoder.dir/requires: CMakeFiles/VideoEncoder.dir/VideoEncoder.cpp.o.requires

.PHONY : CMakeFiles/VideoEncoder.dir/requires

CMakeFiles/VideoEncoder.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/VideoEncoder.dir/cmake_clean.cmake
.PHONY : CMakeFiles/VideoEncoder.dir/clean

CMakeFiles/VideoEncoder.dir/depend:
	cd /home/tiagocm/Documents/Code/video-encoding/cpp/src && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/tiagocm/Documents/Code/video-encoding/cpp/src /home/tiagocm/Documents/Code/video-encoding/cpp/src /home/tiagocm/Documents/Code/video-encoding/cpp/src /home/tiagocm/Documents/Code/video-encoding/cpp/src /home/tiagocm/Documents/Code/video-encoding/cpp/src/CMakeFiles/VideoEncoder.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/VideoEncoder.dir/depend

