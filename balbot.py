import sys
import logging, datetime, json
from nano import Nano
from scheduler import Scheduler

import logging.config
import argparse
import sys, time
from daemon import Daemon
 
#!/usr/bin/env python

import sys, time
from daemon import Daemon

def getparser():
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
	parser.add_argument('--start', dest='start', action='store_true',
                    const=sum, default=max,
                    help='start tiber ')
    parser.add_argument('--restart', dest='restart', action='store_true',
                    const=sum, default=max,
                    help='restart tiber ')
	parser.add_argument('--stop', dest='stop', action='store_true',
                    const=sum, default=max,
                    help='stop tiber ')

class Experiment(Scheduler, Daemon):
    """
    Experiment class
    controls the evolution of the experiment with the Scheduler
    Each parameter can e set through this class
    As many config file as many bots will be created, the bot are stored
    in the 'bots' attribute.
    """
    def __init__(self, *args, **kwargs):
        Scheduler.__init__(self, self.experiment_manager)
        Daemon.__init__(self, *args, **kwargs)
        self.bots=[]
        self.common_file = common_file
        for arg in args:
            nano= Nano(self.dict_from_json(arg),self.dict_from_json(common_file))
            self.bots.append(nano)

    @staticmethod
    def dict_from_json(json_file):
        with open(json_file) as json_data:
            dict_ = json.load(json_data)
        return dict_

    """
    Start the experiment.
    Argument:
    duration -- expressed in seconds
    """
    def start_experiment(self, duration):
        self.routine_manager(duration)
    """
    Do the relevant action for the experiment:
    1) For each nano, at scheduled time, start online experience
    """
    def experiment_manager(self):
        for nano in self.bots:
            for event_time in self.events:
                self.schedule_event(nano.online_experience(),event_time)
                logging.debug("nano {} scheduled at {}".format(nano.name, str(event_time)))
            self.events = []

if __name__ == "__main__":
	args = parser.parse_args()        

	if args.start:
		daemon.start()
	if args.stop:
		daemon.stop()
	if args.restart:
		daemon.restart()
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
    logging.config.fileConfig('logging.ini')
    logging.basicConfig(format='%(asctime)s %(message)s',level=logging.DEBUG)
    log = logging.getLogger("root")

    experiment=Experiment(pidfile)
    experiment.set_hours(Experiment.dict_from_json("sbinzolo.json")['hours'])
    experiment.start_experiment(datetime.timedelta(days=3).total_seconds())

