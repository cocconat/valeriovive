import logging


'''
    NOTSET means inherit the log level from the parent logger
'''

LEVELS = {'debug'   : logging.DEBUG,
          'info'    : logging.INFO,
          'warning' : logging.WARNING,
          'error'   : logging.ERROR,
          'critical': logging.CRITICAL,
         }


def getLevel(lvl):
    return LEVELS.get(lvl) or logging.DEBUG


def get_streamhandler(lvl=None):
    sh = logging.StreamHandler()
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    sh.setFormatter(logging.Formatter(fmt))
    sh.setLevel(getLevel(lvl))
    return sh
