from twitter_agent import TwitterAgent
import tweepy
import json, random
import logging, Logger


class Nano(object):
    def __init__(self, nano_json, target_json):
        self.json_ =nano_json
        self.target_json = target_json
        self.name = self.get_json(self.json_)['name']
        self.nano_conf = self.get_json(self.json_)['conf']
        self.twitter_agent = TwitterAgent(self.nano_conf,self.name)

        self.myStream = tweepy.Stream(auth=self.twitter_agent.api.auth,
                        listener=self.twitter_agent)
        self.mood =[]
        self.buddy_list = []
        self.hash_list  = []
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(Logger.get_streamhandler())
        self.logger.info('created Nano {} obj'.format(self.name))

        self.individual_behaviour(nano_json)


    def individual_behaviour(self, json_):
        self.buddy_list = self.get_json(self.json_)['buddies']
        self.hash_list  = self.get_json(self.json_)['hashtags']
        self.mood       = self.get_json(self.json_)['mood']
        self.get_actions()

    def common_behaviour(self, target_json):
        self.buddy_list = self.get_json(self.target_json)['buddies']
        self.buddy_list = self.get_json(self.target_json)['buddies']
        self.hash_list  = self.get_json(self.target_json)['hashtags']
        self.mood       = self.get_json(self.target_json)['mood']
        self.get_actions()


    def get_actions(self):
        self.actions=[]
        if "search_and_follow" in self.mood:
            self.actions.append(self.twitter_agent.search_and_follow)
        if "search_and_retweet" in self.mood:
            self.actions.append(self.twitter_agent.search_and_retweet)
        # if "retweet_my_friends" in self.mood:
            # self.actions.append(self.twitter_agent.retweet_my_friends)

    @staticmethod
    def get_json(json_file):
        with open(json_file) as json_data:
            nano_conf = json.load(json_data)
        return nano_conf

    def online_experience(self):
        random.shuffle(self.actions)
        for action in self.actions[:2]:
            try:
                action(self.buddy_list, self.hash_list)
            except:
                raise ValueError
                self.logger.error("Online experience it's not working!!! \n")

