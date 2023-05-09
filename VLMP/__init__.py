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

if "-m" not in sys.argv:
    #This done to avoid the error when running the program with -m option.
    #When running with -m option a large number of libraries imported by VLMP
    #are not needed.

    logger.info("Starting VLMP...")

    from .VLMP  import VLMP
    from .utils import *
