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

def liquidLauncher(simulationSetsInfo,nodeGPUList,postScript):

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
                    Node: {nodeId}')

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
                     f"UAMMDlauncher {simSetOptions}\n"
                     f"{postScript}\n")

            f.write(batch)

        subprocess.run(["bsub","-N",jobName,
                        "-q","gpu.q",
                        "-l",f"hostname={nodeId}",
                        "-o",f"{os.getcwd()}/stdout.log",
                        "-e",f"{os.getcwd()}/stderr.log",
                        ".job"])
        time.sleep(1.0)
        os.chdir(cwd)

        ############################################################

    logger.info("All simulation sets job have been submitted")

def slurmLauncher(simulationSetsInfo,nodeList,filling,partitionList,modules,postScript):

    if modules[0] != "":
        modules = " ".join(modules)
        modules = f"module purge\n module load {modules}\n"

    lenNodeList      = len(nodeList)
    lenFilling       = len(filling)
    lenPartitionList = len(partitionList)

    if(lenPartitionList == 1 and lenNodeList >1):
        part = partitionList[0]
        partitionList    = [part]*lenNodeList
        lenPartitionList = len(partitionList)

    if(lenNodeList == 0):
        nodeList = [None]*lenPartitionList
    else:
        if(lenNodeList!=lenPartitionList):
            self.logger.error("The number of nodes and the number of partitions must be the same")
            sys.exit(1)

        if(lenNodeList!=lenFilling):
            self.logger.error("The number of nodes and the number of filling entries must be the same")
            sys.exit(1)

        nodeListTmp      = []
        partitionListTmp = []
        for i,f in enumerate(filling):
            for _ in range(f):
                nodeListTmp.append(nodeList[i])
                partitionListTmp.append(partitionList[i])

        nodeList      = nodeListTmp.copy()
        partitionList = partitionListTmp.copy()

    nodePartitionList = list(zip(nodeList,partitionList))
    nodePartitionList = itertools.cycle(nodePartitionList)

    simulationName  = simulationSetsInfo["name"]
    simulationsInfo = simulationSetsInfo["simulations"]
    simulationSets  = simulationSetsInfo["simulationSets"]

    logger = logging.getLogger("VLMP")

    logger.info("Starting slurm ...")
    logger.info("Simulation name: {}".format(simulationName))

    for jobIndex,[simSetName,simSetFolder,simSetOptions,simSetComponents] in enumerate(simulationSets):
        node,partition = next(nodePartitionList)

        jobName = f"{simulationName}_{simSetName}"

        logger.info(f'Launching simulation ...\n\
                    Job name: \"{jobName}\"\n\
                    Simulation folder: \"{simSetFolder}\"\n\
                    Binary: \"UAMMDlauncher\"\n\
                    Simulation options: \"{simSetOptions}\"\n\
                    Node: \"{node}\"\n\
                    Partition: \"{partition}\"')

        ############################################################

        cwd = os.getcwd()
        os.chdir(simSetFolder)

        if node == None:
            nodeSBATCH = ""
        else:
            nodeSBATCH = f"#SBATCH --nodelist={node}"


        with open("./.job","w") as f:
            batch = ("#!/bin/bash\n"
                     f"#SBATCH --job-name={jobName}\n"
                     f"#SBATCH --partition={partition}\n"
                      "#SBATCH --nodes=1\n"
                      "#SBATCH --ntasks-per-node=1\n"
                      "#SBATCH --cpus-per-task=1\n"
                      "#SBATCH --gres=gpu:1\n"
                      "#SBATCH --output=stdout.log\n"
                      "#SBATCH --error=stderr.log\n"
                     f"{nodeSBATCH}\n"
                     f"{modules}\n"
                     f"UAMMDlauncher {simSetOptions}\n"
                     f"{postScript}\n")

            f.write(batch)

        subprocess.run(["sbatch",".job"])
        time.sleep(1.0)

        os.chdir(cwd)

        ############################################################
    return

if __name__ == "__main__":

    #Create argument parser
    mainParser = argparse.ArgumentParser(description='Run a set of simulations')

    #Add arguments
    mainParser.add_argument('--session', type=str, help='VLMP session info', required=True)

    #There are two simualtions options, local and liquid (cluster lsf). If none is selected, local is used.
    #Add mutually exclusive group
    group = mainParser.add_mutually_exclusive_group()
    group.add_argument('--local' , action='store_true', help='Run simulations locally')
    group.add_argument('--liquid', action='store_true', help='Run simulations in liquid cluster')
    group.add_argument('--slurm' , action='store_true', help='Run simulations in slurm cluster')

    mainArgs,_ = mainParser.parse_known_args()

    parser = argparse.ArgumentParser(parents=[mainParser],add_help=False)
    if mainArgs.local:
        parser.add_argument('--gpu', nargs='+', type=int, help='List of gpu ids to use',required=True)

    if mainArgs.liquid:
        parser.add_argument('--node', nargs='+', type=str, help='List of node ids to use',required=True)
        parser.add_argument('--postScript', type=str, help='Post script to run after simulation',required=False)

    if mainArgs.slurm:
        parser.add_argument('--node', nargs='+', type=str, help='List of node ids to use',required=False)
        parser.add_argument('--partition', nargs='+', type=str, help='List of node ids to use',required=True)
        parser.add_argument('--filling',nargs='+', type=int, help='List of sim per node',required=False)
        parser.add_argument('--modules', nargs='+', type=str, help='List of modules used',required=False)
        parser.add_argument('--postScript', type=str, help='Post script to run after simulation',required=False)

    #Parse arguments
    args = parser.parse_args()

    #########################################################

    #Load simulation sets info
    with open(args.session,"r") as f:
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

    if mainArgs.local:
        logger.info("Running simulations locally ...")
        child_pid = os.fork()

        if child_pid == 0:
            localLauncher(simulationSetsInfo,args.gpu)
        else:
            sys.exit(0)
    elif mainArgs.liquid:
        logger.info("Running simulations in liquid cluster ...")

        postScript = args.postScript if args.postScript else ""
        liquidLauncher(simulationSetsInfo,args.node,postScript)
    elif mainArgs.slurm:
        logger.info("Running simulations in slurm cluster ...")

        if args.node:
            node       = args.node
            filling    = args.filling if args.filling else [1]*len(args.node)
        else:
            if args.filling:
                logger.error("Filling only can be used when a node list is given")
                sys.exit(1)
            node    = []
            filling = []

        if len(node) != len(filling):
            logger.error("The size of node and filling must match")
            sys.exit(1)

        partition  = args.partition
        modules    = args.modules if args.modules else [""]
        postScript = args.postScript if args.postScript else ""
        slurmLauncher(simulationSetsInfo,node,filling,partition,modules,postScript)

    else:
        logger.error("No simulation option selected")
        sys.exit(1)

    sys.exit(0)
