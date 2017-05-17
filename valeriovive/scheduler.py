import json, sched, datetime, time
import logging
import threading
import random

def dict_from_json(json_file):
        with open(json_file) as json_data:
            dict_ = json.load(json_data)
        return dict_

class Scheduler:
    def __init__(self, events_manager):
        self.log = logging.getLogger(__name__)
        self.log.info(" starting {} ".format(__name__))
        self.events = []
        self.hours = []
        self.events_manager = events_manager

    """
    Converts hours in dates.
    Every day convert the hour in the exact date yyyy-mm-dd hh-mm
    """
    @staticmethod
    def events_from_hours(hours):
        if not isinstance(hours, list):
            hours = list(hours)
        events = [datetime.datetime.today().replace(hour=hour,
                                                    minute=random.choice(range(60)))
                                                    for hour in hours]
        return events

    """
    Routine manager
    Always running untill --stop

    conf_file is a path to json file.
    The configuration file is read continously

    """
    def routine_manager(self, conf_file):
        logging.info("routine manager start at {}".format(str(datetime.datetime.now())))
        conf = dict_from_json(conf_file)['common']

        while True and datetime.datetime.now() < datetime.datetime.strptime(conf["end_date"],"%Y-%m-%d"):
            self.events_manager()
            self.log.debug("routine manager loop at {}".format(str(datetime.datetime.now())))
            conf = dict_from_json(conf_file)['common']
            try:
                if conf["scheduler_interval"] == "midnight":
                    interval_seconds = (datetime.datetime.today().replace(hour=23, minute=59) - datetime.datetime.now()).total_seconds()
                    self.log.info("Next routine_manager loop at {}".format(datetime.datetime.today().replace(hour=23, minute=59)))
                if isinstance(conf["scheduler_interval"], int):
                    interval_seconds = datetime.timedelta(hours=conf["scheduler_interval"])
            except KeyError:
                self.log.error("Scheduler properties not found in {}", conf_file)
            time.sleep(interval_seconds)
    """
    Schedule event with threading

    Params:
    ==========
    event_time      datetime format
    action          function
    **kwargs        function arguments
    """

    @staticmethod
    def schedule_event(event_time, action, **kwargs):
        delta = (event_time - datetime.datetime.now()).total_seconds()
        if delta > 0:
            logging.debug("delta is {}".format(delta))
            T = threading.Timer(int(delta), action, **kwargs)
            T.start()
        else:
            logging.debug("event {} scheduled in the past!".format(str(event_time)))


