import sys
import logging, datetime, json
from nano import Nano
from scheduler import Scheduler

import logging.config
import argparse
import sys, time, os
from daemon import Daemon

#!/usr/bin/env python


def getparser():
        parser = argparse.ArgumentParser(description='run TIBER instance')
        parser.add_argument('--conf_file', type=str, default=None,
                            help='configuration_file for the experiment')
        parser.add_argument('--duration', type=int, default=None,
                            help='duration in days of the experiment')
        parser.add_argument('--start', dest='start', action='store_true', default=False,
                    help='start valeriovive ')
        parser.add_argument('--restart', dest='restart', action='store_true',default=False,
                    help='restart valeriovive ')
        parser.add_argument('--stop', dest='stop', action='store_true',default=False,
                    help='stop valeriovive ')
        return parser.parse_args()

class ExperimentDaemon(Daemon):
    def run(self):
        log = logging.getLogger("Daemon")
        args = getparser()
        experiment=Experiment()
        experiment.prepare_experiment(args.conf_file)
        log.debug("Experiment configured with {} and duration {}".format(args.conf_file, args.duration))
        experiment.start_experiment(args.duration)


class Experiment(Scheduler, Daemon):
    """
    Experiment class
    controls the evolution of the experiment with the Scheduler
    Each parameter can e set through this class
    As many config file as many bots will be created, the bot are stored
    in the 'bots' attribute.
    """
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger("root")
        Scheduler.__init__(self, self.events_manager)
        self.bots=[]
        self.conf= None

    """
    Prepare experiment with conf_file params
    """
    def prepare_experiment(self, conf_file=None):
        if isinstance(self.conf, str):
            self.dict_from_json(conf_file)
        else:
            self.log.error("if you re not setting congf file, you are wrong")
            conf_file = (os.getcwd()+'/valeriovive/nani.json')
            self.conf = self.dict_from_json(conf_file)
            self.log.debug("conf file is {}".format(conf_file))

        for agent in self.conf['agents']:
            nano = Nano(self.conf[agent], self.conf['common'])
            self.bots.append(nano)
            self.log.debug("Agent {} found in config file".format(agent))

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
        if duration==None:
            duration=datetime.timedelta(days=1).total_seconds()
        self.log.debug("Experimetn routine starting")
        self.routine_manager(duration)

    """
    Do the relevant action for the experiment:
    1) For each nano, at scheduled time, start online experience
    """
    def events_manager(self):
        for nano in self.bots:
            try:
                nano.events = Scheduler.events_from_hours(nano.conf['hours'])
            except:
                nano.events = Scheduler.events_from_hours(self.conf['common']['hours'])
            for event_time in nano.events:
                self.schedule_event(event_time, nano.online_experience)
                logging.debug("nano {} scheduled at {}".format(nano.name, str(event_time)))

if __name__ == "__main__":
    logging_path=os.getcwd()+'/valeriovive/logging.ini'
    logging.config.fileConfig(logging_path)
    args = getparser()
    exp=ExperimentDaemon("/tmp/valeriovive.pid")

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




