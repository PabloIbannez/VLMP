HOSTNAME=$(shell hostname)

ifeq ($(HOSTNAME), pablo-HOME)
	ARCH=86
	CXX=g++
	STD=17
	
	CUDA_ROOT=/usr/local/cuda
	NVCC=$(CUDA_ROOT)/bin/nvcc
	
	UAMMD_ROOT=/home/pablo/Desktop/UAMMD/
	UAMMD_STRUCTURED_ROOT=$(UAMMD_ROOT)/extensions/structured/
	
	INCLUDE_FLAGS= -I$(CUDA_ROOT)/include -I$(UAMMD_ROOT)/src/ -I$(UAMMD_ROOT)/src/third_party/ -I$(UAMMD_STRUCTURED_ROOT)
	LIBRARIES=
else ifeq ($(HOSTNAME), liquid.ftmc.uam.es)
	ARCH=60 61 75
	CXX=g++
	STD=14

	CUDA_ROOT=/usr/local/cuda
	NVCC=nvcc
	
	UAMMD_ROOT=/home/pablo/UAMMD/
	UAMMD_STRUCTURED_ROOT=$(UAMMD_ROOT)/extensions/structured/
	
	INCLUDE_FLAGS= -I$(CUDA_ROOT)/include -I$(UAMMD_ROOT)/src/ -I$(UAMMD_ROOT)/src/third_party/ -I$(UAMMD_STRUCTURED_ROOT)
	LIBRARIES=-lstdc++fs
endif

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

launcher:
	$(NVCC) --expt-relaxed-constexpr --expt-extended-lambda -std=c++$(STD) -O3 $(OPTIONS) -ccbin="$(CXX)" -Xcompiler="$(CPU)" $(GENCODE_FLAGS) UAMMDlauncher.cu $(INCLUDE_FLAGS) $(LIBRARIES) -o UAMMDlauncher
	mv UAMMDlauncher ../../../../bin/
