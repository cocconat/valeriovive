import logging
from experiment import ExperimentDaemon
import sys,argparse, os

def getparser():
        parser = argparse.ArgumentParser(description='run TIBER instance')
        parser.add_argument('--conf_file', type=str, default=None,
                            help='configuration_file for the experiment')
        parser.add_argument('--start', dest='start', action='store_true', default=False,
                    help='start valeriovive ')
        parser.add_argument('--restart', dest='restart', action='store_true',default=False,
                    help='restart valeriovive ')
        parser.add_argument('--stop', dest='stop', action='store_true',default=False,
                    help='stop valeriovive ')
        return parser.parse_args()


if __name__ == "__main__":
    logging_path=os.getcwd()+'/valeriovive/logging.ini'
    logging.config.fileConfig(logging_path)
    args = getparser()
    exp=ExperimentDaemon("/tmp/valeriovive.pid", args)

    if args.start:
        exp.start()
        sys.exit(0)
    elif args.restart:
        exp.restart()
        sys.exit(0)
    elif args.stop:
        exp.stop()
        sys.exit(0)
    else:
        print ("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)



