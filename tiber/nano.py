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
    '''
    def __init__(self, nano_conf, common_conf):
        self.common_conf = common_conf
        self.own_conf = nano_conf
        self.name = self.own_conf['name']
        self.nano_conf = self.own_conf['conf']
        self.twitter_agent = TwitterAgent(self.nano_conf,self.name)
        self.mood =[]
        self.buddy_list = []
        self.hash_list  = []
        self.events=None
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(Logger.get_streamhandler())
        self.logger.info('created Nano {} obj'.format(self.name))
        self.set_behaviour(self.common_conf)

    def set_behaviour(self, dict_):
        self.buddy_list = dict_['buddies']
        self.hash_list  = dict_['hashtags']
        self.mood       = dict_['mood']
        self.get_actions()

    def get_actions(self):
        self.actions=[]
        if "search_and_follow" in self.mood:
            self.actions.append(self.twitter_agent.search_and_follow)
        if "search_and_retweet" in self.mood:
            self.actions.append(self.twitter_agent.search_and_retweet)
        # if "retweet_my_friends" in self.mood:
            # self.actions.append(self.twitter_agent.retweet_my_friends)

    def online_experience(self):
        random.shuffle(self.actions)
        for action in self.actions:
            try:
                action(self.buddy_list, self.hash_list)
            except:
                self.logger.error("Online experience it's not working!!! \n")

