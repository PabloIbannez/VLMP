import sys,os

import logging

import json

import argparse

from .utils.launcher import *

if __name__ == "__main__":

    #Create argument parser
    mainParser = argparse.ArgumentParser(description='Run a set of simulations')

    #Add arguments
    mainParser.add_argument('--session', type=str, help='VLMP session info', required=True)

    #There are two simualtions options, local and liquid (cluster lsf). If none is selected, local is used.
    #Add mutually exclusive group
    group = mainParser.add_mutually_exclusive_group()
    group.add_argument('--rebuild' , action='store_true', help='Rebuild results')
    group.add_argument('--local'   , action='store_true', help='Run simulations locally')
    group.add_argument('--liquid'  , action='store_true', help='Run simulations in liquid cluster')
    group.add_argument('--slurm'   , action='store_true', help='Run simulations in slurm cluster')

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

    #Add file handler to logger
    logger.addHandler(fileHandler)

    logger.info("Starting VLMP ...")

    if mainArgs.rebuild:
        logger.info("Rebuilding results folders ...")
        rebuildResults(simulationSetsInfo)

    elif mainArgs.local:
        #Remove console handler
        logger.removeHandler(logger.handlers[0])

        logger.info("Running simulations locally ...")
        child_pid = os.fork()

        if child_pid == 0:
            localLauncher(simulationSetsInfo,args.gpu)
        else:
            sys.exit(0)
    elif mainArgs.liquid:
        #Remove console handler
        logger.removeHandler(logger.handlers[0])

        logger.info("Running simulations in liquid cluster ...")

        postScript = args.postScript if args.postScript else ""
        liquidLauncher(simulationSetsInfo,args.node,postScript)
    elif mainArgs.slurm:
        #Remove console handler
        logger.removeHandler(logger.handlers[0])

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
