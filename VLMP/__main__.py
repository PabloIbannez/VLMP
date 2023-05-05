import sys,os

import logging

import json

import shutil

import argparse

import itertools

import psutil
import signal

import multiprocessing
import subprocess

import time
import datetime

def associateCPUtoGPU(gpuIDList):
    cpuName = multiprocessing.current_process().name
    try:
        cpuID = int(cpuName[cpuName.find('-') + 1:]) - 1
    except:
        cpuID = 0
    gpuID = gpuIDList[cpuID % len(gpuIDList)]
    return gpuID

def runSimulation(simulationsInfo, setInfo, gpuIDList):

    name, folder, options, components = setInfo

    gpuId = associateCPUtoGPU(gpuIDList)
    cudaFlag = 'CUDA_VISIBLE_DEVICES={}'.format(gpuId)

    fout = open(folder+"/stdout.log","w")
    ferr = open(folder+"/stderr.log","w")

    sst = time.time()

    sim = " ".join([cudaFlag, " ".join(["UAMMDlauncher",options])])
    simReturn = subprocess.run(sim, stdout=fout, stderr=ferr, shell=True, cwd=folder)

    fout.close()
    ferr.close()

    if simReturn.returncode == 0:
        logger.info("Simulation {} finished. Total time: {}".format(folder,
                                                                    str(datetime.timedelta(seconds=(time.time() - sst)))))
    else:
        logger.info("Simulation {} finished with errors. Error code: {}. Total time: {}".format(folder,
                                                                                                simReturn.returncode,
                                                                                                str(datetime.timedelta(seconds=(time.time() - sst)))))
    return simReturn

def runSimulationSets(logger, simulationsInfo, simulationSets, gpuIDList):

    with multiprocessing.Pool(processes=len(gpuIDList)) as pool:
        simSetGPU = tuple(zip(itertools.repeat(simulationsInfo.copy()),simulationSets,itertools.repeat(gpuIDList)))
        out = list(pool.starmap(runSimulation,simSetGPU))

    return out

def localLauncher(simulationSetsInfo,gpuIDList):

    simulationName  = simulationSetsInfo["name"]
    simulationsInfo = simulationSetsInfo["simulations"]
    simulationSets  = simulationSetsInfo["simulationSets"]

    logger = logging.getLogger("VLMP")

    logger.info("Start local ...")
    logger.info("Simulation name: {}".format(simulationName))
    logger.info("pid: {}".format(os.getpid()))

    def signalHandler(sig,frame):
        logger.info("Signal {} detected. Exiting ...".format(sig))

        mainProcess = psutil.Process(os.getpid())
        for child in mainProcess.children(recursive=True):
            child.kill()

        sys.exit(0)

    signal.signal(signal.SIGINT,signalHandler)
    signal.signal(signal.SIGTERM,signalHandler)

    st = time.time()
    out = runSimulationSets(logger,simulationsInfo,simulationSets,gpuIDList)
    logger.info("Simulation sets finished. Total time: {}".format(str(datetime.timedelta(seconds=(time.time() - st)))))

    for i in out:
        if(i.returncode!=0):
            logger.error("Something went wrong for simulation: {}".format(i))

    logger.info("End")

def liquidLauncher(simulationSetsInfo,nodeGPUList):

    nodeGPUList = itertools.cycle(nodeGPUList)

    user = os.environ.get("USER")

    simulationName  = simulationSetsInfo["name"]
    simulationsInfo = simulationSetsInfo["simulations"]
    simulationSets  = simulationSetsInfo["simulationSets"]

    logger = logging.getLogger("VLMP")

    logger.info("Starting liquid ...")
    logger.info("Simulation name: {}".format(simulationName))

    for jobIndex,[simSetName,simSetFolder,simSetOptions,simSetComponents] in enumerate(simulationSets):
        nodeId = next(nodeGPUList)
        jobName = f"{simulationName}_{simSetName}"

        logger.info(f'Launching simulation ...\n\
                    Job name: \"{jobName}\"\n\
                    Simulation folder: \"{simSetFolder}\"\n\
                    Binary: \"UAMMDlauncher\"\n\
                    Simulation options: \"{simSetOptions}\"\n\
                    Node: compute-0-{nodeId}')

        ############################################################

        cwd = os.getcwd()
        os.chdir(simSetFolder)

        with open("./.job","w") as f:
            batch = ("#!/bin/bash\n"
                     "#$ -S /bin/bash\n"
                     f"#$ -N {jobName}\n"
                     "#$ -cwd\n"
                     "#$ -o stdout.log\n"
                     "#$ -e stderr.log\n"
                     "#$ -l gpu=1\n"
                     "#$ -V\n"
                     f"cd /scratch/{user}/{jobName}-$JOB_ID\n"
                     "module load gcc/8.4 cuda/10.2\n"
                     f"UAMMDlauncher {simSetOptions}\n")

            f.write(batch)

        subprocess.run(["bsub","-N",jobName,
                        "-q","gpu.q",
                        "-l",f"hostname=compute-0-{nodeId}",
                        "-o",f"{os.getcwd()}/stdout.log",
                        "-e",f"{os.getcwd()}/stderr.log",
                        ".job"])
        time.sleep(1.0)
        os.chdir(cwd)

        ############################################################

    logger.info("All simulation sets job have been submitted")

if __name__ == "__main__":

    #Create argument parser
    parser = argparse.ArgumentParser(description='Run a set of simulations')

    #Add arguments
    parser.add_argument('-s', '--simulationSetsInfo', type=str, help='Simulation sets info file', required=True)

    #There are two simualtions options, local and liquid (cluster lsf). If none is selected, local is used.
    #Add mutually exclusive group
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--local', action='store_true', help='Run simulations locally')
    group.add_argument('--liquid', action='store_true', help='Run simulations in liquid cluster')

    parser.add_argument('--gpu', nargs='+', type=int, help='List of gpu ids to use',required=True)

    #Parse arguments
    args = parser.parse_args()

    #Load simulation sets info
    with open(args.simulationSetsInfo,"r") as f:
        simulationSetsInfo = json.load(f)

    #Start VLMP

    logger = logging.getLogger("VLMP")

    #Add file handler to logger
    fileHandler = logging.FileHandler(simulationSetsInfo["name"]+".log","w")
    #Set the same level as the logger
    fileHandler.setLevel(logger.level)
    #Get the same formatter as the logger
    fileHandler.setFormatter(logger.handlers[0].formatter)

    #Remove console handler
    logger.removeHandler(logger.handlers[0])
    #Add file handler to logger
    logger.addHandler(fileHandler)

    logger.info("Starting VLMP ...")

    if args.local or not args.liquid:
        logger.info("Running simulations locally ...")
        child_pid = os.fork()

        if child_pid == 0:
            localLauncher(simulationSetsInfo,args.gpu)
        else:
            sys.exit(0)
    else:
        logger.info("Running simulations in liquid cluster ...")
        liquidLauncher(simulationSetsInfo,args.gpu)

    sys.exit(0)
