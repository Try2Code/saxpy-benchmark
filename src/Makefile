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
CFLAGS = -std=c++11 -Ofast -march=native -mtune=native -funroll-loops -mfpmath=both
EXE =
RM = rm -f


###################################################################
# Step 2: Select which implementations to enable
################################################################### 
TARGETS = saxpy_cpu$(EXE) \
	  SaxpyLoop.class \
	  saxpy_cuda$(EXE) \
	  saxpy_omp$(EXE) \
	  saxpy_thrust$(EXE) \
	  saxpy_cublas$(EXE)

###################################################################
# Step 3: Configure additional settings for the SDKs
###################################################################

#
# CUDA settings
#
#CUDA_CFLAGS = -O3 -std=c++11 -Wno-deprecated-gpu-targets --x cu
CUDA_CFLAGS = -std=c++11 -Wno-deprecated-gpu-targets --x cu -O2
CUDA_LDFLAGS =

#CUDA_CFLAGS =
#CUDA_LDFLAGS =


#
# OpenMP settings
# Linux
OMP_CFLAGS = -O3 -std=c++11 -fopenmp
OMP_LDFLAGS = 

###################################################################
# Done. 
# Usually you don't need to change anything beyond this point
###################################################################

all: $(TARGETS)
	cd ../results && $(MAKE)

saxpy_cpu$(EXE): saxpy_cpu.cpp saxpy.h
	$(CC) $(CFLAGS) $(CC_O) $(@) saxpy_cpu.cpp

saxpy_cuda$(EXE): saxpy_cuda.cpp saxpy.h
	nvcc $(CUDA_CFLAGS) $(CUDA_LDFLAGS) -o saxpy_cuda$(EXE) saxpy_cuda.cpp
		
saxpy_omp$(EXE): saxpy_omp.cpp saxpy.h
	$(CC) $(OMP_CFLAGS) $(OMP_LDFLAGS) saxpy_omp.cpp $(CC_O) $(@) 

saxpy_thrust$(EXE): saxpy_thrust.cpp saxpy.h
	nvcc $(CUDA_CFLAGS) $(CUDA_LDFLAGS) -o saxpy_thrust$(EXE) saxpy_thrust.cpp
		
saxpy_cublas$(EXE): saxpy_cublas.cpp saxpy.h
	nvcc $(CUDA_CFLAGS) $(CUDA_LDFLAGS) -o saxpy_cublas$(EXE) saxpy_cublas.cpp -lcublas
		
saxpy_bulk$(EXE): saxpy_bulk.cpp saxpy.h
	nvcc $(CUDA_CFLAGS) $(BULK_CFLAGS) $(CUDA_LDFLAGS) -o saxpy_bulk$(EXE) saxpy_bulk.cpp
		
SaxpyLoop.class: SaxpyLoop.java
	javac SaxpyLoop.java
	
clean:
	$(RM) $(TARGETS) *.lib *.a *.exe *.obj *.o *.exp *.pyc

