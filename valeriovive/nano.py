from twitter_agent import TwitterAgent
import tweepy
import json, random
import logging, Logger


class Nano(object):
    '''
    Create Nano Object
    Nano is the active element of the experiment,it does stuff
    nano will be initialited with the common and the private conf
    nano has no perception of time.

    Attributes
    ==========
    CONF:
    common_conf dict_from_json  See README
    own_conf    dict_from_json  See README

    __twitter_agent TwitterAgent(Tweepy)

    Behaviour:
    actions         set of __twitter agent methods
    buddy_list      list(strigs)
    hash_list
    events          list(hours(int[0-23]))

    Methods
    ===========


    '''
    def __init__(self, conf, common_conf):
        self.common_conf = common_conf
        self.__nano_conf = nano_conf
        self.__twitter_agent = TwitterAgent(self.nano_conf,self.conf['name'])
        self.actions =[]
        ###
        self.buddy_list = []
        self.hash_list  = []
        self.events=None
        self.set_behaviour(self.common_conf)

        ### loggers
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(Logger.get_streamhandler())
        self.logger.info('created Nano {} obj'.format(self.conf['name']))


    """
    Set behaviour

    Dict needs to contain buddies , hashtags , actions
    """
    def set_behaviour(self, dict_):
        self.buddy_list = dict_['buddies']
        self.hash_list  = dict_['hashtags']
        self.actions       = dict_['actions']
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
        self.__twitter_agent.get_timeline()
        for action in self.actions:
            try:
                action(self.buddy_list, self.hash_list)
            except:
                self.logger.error("Online experience it's not working!!! \n")

