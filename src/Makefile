#
# Instructions:
#  You need to do three steps, see below
#

###################################################################
# Step 1: Configure your host compiler
###################################################################

# Linux/MacOS/Unix tools
CC = g++
CC_O = -o
#CFLAGS = -O3 -std=c++11
CFLAGS = -std=c++11 -Ofast -march=native -mtune=native -funroll-loops -mfpmath=both -fno-use-linker-plugin
EXE =
RM = rm -f

CLANG_FLAGS = -fopenmp  -fopenmp-targets=nvptx64-nvidia-cuda -v
# OpenMP settings
# Linux
OMP_CFLAGS = -O3 -std=c++11 -fopenmp -fno-use-linker-plugin
OMP_LDFLAGS = 

###################################################################
# Step 2: Select which implementations to enable
################################################################### 
CPU_TARGETS = saxpy_cpu$(EXE) \
	  saxpy_omp$(EXE)

GPU_TARGETS = saxpy_cuda$(EXE) \
 	  saxpy_thrust$(EXE) \
 	  saxpy_cublas$(EXE)

###################################################################
# Step 3: Configure additional settings for the SDKs
###################################################################

#
# CUDA settings
CUDA_CFLAGS = -std=c++11 -Wno-deprecated-gpu-targets --x cu -O2
CUDA_LDFLAGS =

###################################################################
# Done. 
# Usually you don't need to change anything beyond this point
###################################################################

all: $(CPU_TARGETS)

gpu: $(GPU_TARGETS)

# CPU targets
saxpy_cpu$(EXE): saxpy_cpu.cpp saxpy.h
	$(CC) $(CFLAGS) $(CC_O) $(@) saxpy_cpu.cpp
		
saxpy_omp$(EXE): saxpy_omp.cpp saxpy.h
	$(CC) $(OMP_CFLAGS) $(OMP_LDFLAGS) saxpy_omp.cpp $(CC_O) $(@) 
# GPU targets
saxpy_cuda$(EXE): saxpy_cuda.cpp saxpy.h
	nvcc $(CUDA_CFLAGS) $(CUDA_LDFLAGS) -o saxpy_cuda$(EXE) saxpy_cuda.cpp

saxpy_thrust$(EXE): saxpy_thrust.cpp saxpy.h
	nvcc $(CUDA_CFLAGS) $(CUDA_LDFLAGS) -o saxpy_thrust$(EXE) saxpy_thrust.cpp
		
saxpy_cublas$(EXE): saxpy_cublas.cpp saxpy.h
	nvcc $(CUDA_CFLAGS) $(CUDA_LDFLAGS) -o saxpy_cublas$(EXE) saxpy_cublas.cpp -lcublas
		
SaxpyLoop.class: SaxpyLoop.java
	javac SaxpyLoop.java
	
clean:
	$(RM) $(CPU_TARGETS) $(GPU_TARGETS) *.lib *.a *.exe *.obj *.o *.exp *.pyc

