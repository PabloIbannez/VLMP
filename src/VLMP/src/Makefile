ARCH=86
CXX=g++

CUDA_ROOT=/usr/local/cuda
NVCC=$(CUDA_ROOT)/bin/nvcc

UAMMD_ROOT=/home/pablo/Desktop/UAMMD
UAMMD_STRUCTURED_ROOT=$(UAMMD_ROOT)/extensions/structured/

#Uncomment to compile in double precision mode, single by default
#DOUBLE_PRECISION=-DDOUBLE_PRECISION

#This flag controls UAMMD's verbosity, 5 is standard messages, 15 is the maximum debug log level and 0 will only print critical errors. 
LOG_LEVEL=7

#Uncomment to add debug flags to nvcc
#DEBUG=  -src-in-ptx -G  -g

$(foreach sm,$(ARCH),$(eval GENCODE_FLAGS += -gencode arch=compute_$(sm),code=sm_$(sm)))

#Flags to $(CXX)
CPU= -O3 -march=native -fPIC 

OPTIONS=$(DOUBLE_PRECISION) -DMAXLOGLEVEL=$(LOG_LEVEL) $(DEBUG) -DUAMMD_EXTENSIONS

INCLUDE_FLAGS= -I$(CUDA_ROOT)/include -I$(UAMMD_ROOT)/src/ -I$(UAMMD_ROOT)/src/third_party/ -I$(UAMMD_STRUCTURED_ROOT)
LIBRARIES=

vlmp:
	$(NVCC) --expt-relaxed-constexpr --expt-extended-lambda -std=c++17 -O3 $(OPTIONS) -ccbin="$(CXX)" -Xcompiler="$(CPU)" $(GENCODE_FLAGS) VLMP.cu $(INCLUDE_FLAGS) $(LIBRARIES) -o VLMP
	mv VLMP ../bin
