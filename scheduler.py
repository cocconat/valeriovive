import json, sched, datetime
import logging, Logger
import threading
import random

log = logging.getLogger(__name__)

class Scheduler:
    def __init__(self, events_manager):
        log.info(" starting {} ".format(__name__))
        self.events=[]
        self.hours=[]
        self.events_manager=events_manager


    def set_hours(self,hours):
        if not isinstance(hours, list):
            hours = list(hours)
        self.hours = hours

    def routine_manager(self, duration):
        self.daily_events_update()
        start_time=datetime.datetime.now()
        self.events_manager()
        if (datetime.datetime.now()-start_time).total_seconds() < duration:
            duration = duration-datetime.timedelta(days=1).total_seconds()
            threading.Timer(datetime.timedelta(days=1).total_seconds(),self.routine_manager,duration)
            logging.debug("reschedule with new duration {}".format(duration))

    '''
        compute the events of the day.
    '''
    def daily_events_update(self):
        for hour in self.hours:
            self.events.append(datetime.datetime.today().replace(hour=hour, minute=random.choice(range(60))))
        logging.debug("schedule_events are {}".format(self.events))


    @staticmethod
    def schedule_event(action, event_time):
        delta = (event_time - datetime.datetime.now()).total_seconds()
        if delta > 0:
            T = threading.Timer(delta, action)
            T.start()
        else:
            logging.warning("event scheduled in the past!")


