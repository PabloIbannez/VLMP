import sys,os

import logging

import json

################### DEBUG MODE ##################

DEBUG_MODE = True

################# SET UP LOGGER #################

class CustomFormatter(logging.Formatter):

    white = "\x1b[37;20m"
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format     = "%(asctime)s - %(name)s - %(levelname)s - %(message)s "
    formatLine = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: white + formatLine + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + formatLine + reset,
        logging.CRITICAL: bold_red + formatLine + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt,datefmt='%d/%m/%Y %H:%M:%S')
        return formatter.format(record)

logger = logging.getLogger("VLMP")
logger.handlers = []
logger.setLevel(logging.DEBUG)

clogger = logging.StreamHandler()
if DEBUG_MODE:
    clogger.setLevel(logging.DEBUG) #<----
else:
    clogger.setLevel(logging.INFO) #<----

clogger.setFormatter(CustomFormatter())
logger.addHandler(clogger)

#################################################

if __name__ == "__main__":

    #Launcher

    import shutil

    import argparse

    import itertools

    import psutil
    import signal

    import multiprocessing
    import subprocess

    import time
    import datetime

    def localLauncher(simulationSetsInfo,gpuIDList):

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

    #Create argument parser
    parser = argparse.ArgumentParser(description='Run a set of simulations')

    #Add arguments
    parser.add_argument('-s', '--simulationSetsInfo', type=str, help='Simulation sets info file', required=True)

    #There are two simualtions options, local and liquid (cluster lsf). If none is selected, local is used.
    #Add mutually exclusive group
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--local', action='store_true', help='Run simulations locally')
    group.add_argument('--liquid', action='store_true', help='Run simulations in liquid cluster')

    #Read a list of intergers (the gpu ids) from an argument

    group.add_argument('--gpuList', nargs='+', type=int, help='List of gpu ids to use')

    #Parse arguments
    args = parser.parse_args()

    #Start VLMP

    logger = logging.getLogger("VLMP")

    #Add file handler to logger

    with open(args.simulationSetsInfo,"r") as f:
        simulationSetsInfo = json.load(f)

    fileHandler = logging.FileHandler(simulationSetsInfo["name"]+".log")
    #Set the same level as the logger
    fileHandler.setLevel(logger.level)
    #Get the same formatter as the logger
    fileHandler.setFormatter(logger.handlers[0].formatter)
    #Add file handler to logger
    logger.addHandler(fileHandler)

    logger.info("Starting VLMP ...")

    if args.local or not args.liquid:
        logger.info("Running simulations locally ...")
        child_pid = os.fork()

        if child_pid == 0:
            launchLocal(simulationSetsInfo,args.gpuList)
        else:
            sys.exit(0)
    else:
        logger.info("Running simulations in liquid cluster ...")
        launchLiquid(simulationSetsInfo,args.gpuList)

    sys.exit(0)

from .VLMP  import VLMP
from .utils import *

