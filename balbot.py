import sys
import logging
from nano import Nano
from scheduler import Scheduler
import Logger

import multiprocessing

#logging.basicConfig(filename='balbot.log',level=logging.DEBUG)
#logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    root = logging.getLogger()
    root.info('Balbot started')
    root.addHandler(Logger.get_streamhandler('debug'))
    sbinzolo = Nano("sbinzolo.json", "sbinzolo.json")
