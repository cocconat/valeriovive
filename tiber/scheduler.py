import json, sched, datetime, time
import logging, Logger
import threading
import random


class Scheduler:
    def __init__(self, events_manager):
        self.log = logging.getLogger(__name__)
        self.log.info(" starting {} ".format(__name__))
        self.events=[]
        self.hours=[]
        self.events_manager=events_manager

    @staticmethod
    def events_from_hours(hours):
        if not isinstance(hours, list):
            hours = list(hours)
        events =[datetime.datetime.today().replace(hour=hour, minute=random.choice(range(60))) for hour in hours]
        return events

    def routine_manager(self, duration):
        start_time=datetime.datetime.now()
        while True and (datetime.datetime.now()-start_time).total_seconds() < duration:
            self.events_manager()
            logging.debug("routin manager at {}".format(str(datetime.datetime.now())))
            seconds_to_midnight = (datetime.datetime.today().replace(hour=23, minute=59) - datetime.datetime.now()).total_seconds()
            time.sleep(seconds_to_midnight)

    @staticmethod
    def schedule_event(event_time, action):
        delta = (event_time - datetime.datetime.now()).total_seconds()
        if delta > 0:
            logging.debug("delta is {}".format(delta))
            T = threading.Timer(int(delta), action)
            T.start()
        else:
            logging.debug("event {} scheduled in the past!".format(str(event_time)))


