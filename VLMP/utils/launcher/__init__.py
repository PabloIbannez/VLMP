import sys,os

import logging

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

    logger = logging.getLogger("VLMP")

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

    jobIds = []

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

        print("Launching job: {}".format(jobName))

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

        result = subprocess.run(["sbatch", ".job"], capture_output=True, text=True)

        # The output is in result.stdout
        if result.returncode == 0:  # Checking if the sbatch command was successful
            output = result.stdout.strip()
            # The job ID is typically in the format "Submitted batch job <job_id>"
            if "Submitted batch job" in output:
                job_id = output.split()[-1]  # Extracting the job ID from the output
                logger.info(f"Job submitted successfully. Job ID: {job_id}")
                jobIds.append(job_id)
            else:
                logger.error("Failed to submit job")
                logger.error(output)
                sys.exit(1)
        else:
            logger.error("Failed to submit job")
            logger.error(result.stderr)
            sys.exit(1)

        time.sleep(1.0)

        os.chdir(cwd)

        ############################################################
    return jobIds

def rebuildResults(simulationSetsInfo):

    logger = logging.getLogger("VLMP")

    #Check if results folder exists
    if os.path.exists("results"):
        logger.error("The results folder already exists")
        sys.exit(1)
    else:
        os.mkdir("results")

    simulationName  = simulationSetsInfo["name"]
    simulationsInfo = simulationSetsInfo["simulations"]
    simulationSets  = simulationSetsInfo["simulationSets"]

    for simName,simSet,simResult,_ in simulationsInfo:
        #Create a symbolic link to the simulation results
        os.symlink(f"../{simSet}",f"./{simResult}")

