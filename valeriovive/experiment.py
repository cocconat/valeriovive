import sys
import logging
from valeriovive.nano import Nano
from valeriovive.scheduler import Scheduler,dict_from_json

import logging.config
import sys, time, os
from valeriovive.daemon import Daemon

#!/usr/bin/env python

class ExperimentDaemon(Daemon):
    def run(self):
        log = logging.getLogger("Daemon")
        experiment=Experiment()
        experiment.prepare_experiment(self.args.conf_file)
        log.debug("Experiment configured with {}".format(self.args.conf_file ))
        experiment.start_experiment()


class Experiment(Scheduler):
    """
    Experiment classs
    controls the evolution of the experiment with the Scheduler
    Each parameter can e set through this class
    As many config file as many bots will be created, the bot are stored
    in the 'bots' attribute.
    """
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger("root")
        Scheduler.__init__(self, self.events_manager)
        self.bots=[]
        self.conf_dict= None
        self.conf_file=None

    """
    Prepare experiment with conf_file params
    """
    def prepare_experiment(self, conf_file=None):

        ##set the conf file or use the default
        if isinstance(conf_file, str):
            self.conf_dict = dict_from_json(conf_file)
            self.conf_file = conf_file
        else:
            self.log.error("if you re not setting congf file, you are wrong")
            self.conf_file = (os.getcwd()+'/valeriovive/nani.json')
            self.conf = dict_from_json(self.conf_file)
            self.log.debug("conf file is {}".format(self.conf_file))

        ##pass the conf file to each agent
        for agent in self.conf['agents']:
            nano = Nano(agent, self.conf_file)
            self.bots.append(nano)
            self.log.debug("Agent {} found in config file".format(agent))

    """
    Start the experiment.
    Argument:
    duration -- expressed in seconds
    """
    def start_experiment(self):
        self.log.debug("Experimetn routine starting")
        self.routine_manager(self.conf_file)

    def common_hours(self):
        return self.conf['common']['hours']
    """
    Do the relevant action for the experiment:
    1) For each nano, at scheduled time, start online experience
    """
    def events_manager(self):
        for nano in self.bots:
            nano.set_behaviour()
            ##retrieve action hours
            try:
                nano.events = Scheduler.events_from_hours(nano.get_hours())
            except:
                nano.events = Scheduler.events_from_hours(self.common_hours())
            ##schedule actions
            for event_time in nano.events:
                self.schedule_event(event_time, nano.online_experience)
                logging.debug("nano {} scheduled at {}".format(nano.name, str(event_time)))



