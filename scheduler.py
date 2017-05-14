import json, sched, datetime
import logging, Logger

class Scheduler:
    def __init__(self, *argv):
        self.logger = logging.getLogger('Twitter Agent {}'.format(self.name))
        self.logger.info('created Logger'.format(self.name))
        self.time = datetime
        self.scheduler = sched.scheduler(self.time, self.time.sleep)

    def set_hours(self,hours):
        if not isinstance(hour,list):
            hours = list(hours)
        self.hours=hours

    def set_events(self, evnts_time_list):
        today = self.time.date.today()

    def __run_experiment__():
        logging.info("Experiment running at time {} with {} active bots".format(time.time(),len(self.active_bots_json)))

