from twitter_agent import TwitterAgent
import tweepy
import json, random
import logging
from scheduler import dict_from_json


class Nano(object):
    '''
    Create Nano Object
    Nano is the active element of the experiment,it does stuff
    nano will be initialited with the common and the private conf
    nano has no perception of time.

    Attributes
    ==========
    CONF:
    common_conf dict  See README
    own_conf    dict  See README

    __twitter_agent TwitterAgent(Tweepy)

    Behaviour:
    actions         set of __twitter agent methods
    buddy_list      list(strigs)
    hash_list
    events          list(hours(int[0-23]))

    Methods
    ===========


    '''
    def __init__(self, name, conf_file):
        self.name=name
        self.conf_file=conf_file
        self.twitter_agent = TwitterAgent(name)
        self.actions =[]
        ###
        self.buddy_list = []
        self.hash_list  = []
        self.events=None

        ### loggers
        self.logger = logging.getLogger(__name__)
        self.logger.info('created Nano {} obj, and file {}'.format(self.name,conf_file))

    # def twitter_conf(conf_file):
        # try:
            # return dict_from_json(conf_file)[self.name]["twitter"]
        # except KeyError:
            # raise ValueError("missing twitter conf in the configuration file")
    """
    Set behaviour

    Dict needs to contain buddies , hashtags , actions
    """
    def set_behaviour(self):
        self.buddy_list = dict_from_json(self.conf_file)[self.name]['buddies']
        self.hash_list  = dict_from_json(self.conf_file)[self.name]['hashtags']
        self.actions    = dict_from_json(self.conf_file)[self.name]['actions']
        self.get_actions()

    def get_actions(self):
        self.actions=[]
        if "search_and_follow" in self.actions:
            self.actions.append(self.__twitter_agent.search_and_follow)
        if "search_and_retweet" in self.actions:
            self.actions.append(self.__twitter_agent.search_and_retweet)
        if "get_user_timeline" in self.actions:
            self.actions.append(self.__twitter_agent.get_user_timeline)
        # if "retweet_my_friends" in self.actions:
            # self.actions.append(self.__twitter_agent.retweet_my_friends)

    """
    Start Online Session
    log with tweepy and do stuff as in behaviour
    """
    def online_experience(self):
        random.shuffle(self.actions)
        if not self.twitter_agent.connect(dict_from_json[self.name]["twitter"]):
            self.log.error("cannot connect to Twitter!")
        self.twitter_agent.get_timeline()
        for action in self.actions:
            try:
                action(self.buddy_list, self.hash_list)
            except:
                self.logger.error("Online experience it's not working!!! \n")

