import tweepy
from tweepy import OAuthHandler
import tweepy.streaming
from tweepy import StreamListener
from pymongo import MongoClient
import logging, Logger
import random

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

class TwitterAgent(tweepy.StreamListener):
    "twitter_agent class, initiated with keys"
    '''
    TwitterAgent get init with a dictionary
    '''
    def __init__(self, conf, name):
        ##cfg is a json with
            #consumer_key
            #consumer_set
            #access_token
            #secret_token
        self.name=name
        self.cfg=conf
        self.api=None
        self.userdb=None
        self.tweetsdb=None
        self.api, self.auth =self.authenticate(self.cfg)
        self.db_instance()
        self.ERROR=[]
        self.listener = MyStreamListener()
        self.streamer = tweepy.Stream(auth=self.auth, listener=self.listener)
        # logging.propagate(False)

        self.logger = logging.getLogger('Twitter Agent {}'.format(self.name))
        self.logger.info('created Twitter Agent{} obj'.format(self.name))
    ##Authenticate 3 twitter app as a list, the object will rotate for accelerate the download,
    #as it's done can be easily increased number of api

    def authenticate(self,cfg):
        auth=OAuthHandler(cfg["consumer_key"],cfg["consumer_set"])
        auth.set_access_token(cfg["access_token"],cfg["secret_token"])
        return tweepy.API(auth), auth


    #instanciate the database, a dictionary type has been choosen
    #tweetsdb will cotain the whole tweet
    #userdb will contain tweets's authors and relative followers
    def db_instance(self):
        client=MongoClient('localhost', 27017)
        try:
            db=client.get_database('dict')
            self.userdb=db[self.name]
            self.tweetsdb=db['received_tweets']
            #error list it's for those user resulting missing to followers retrieve
        except:
            raise ValueError("Error during mongodb initialization")

    def add_friends(self, buddy_list, hash_list):
        self.logger.debug("add_friends")
        if not isinstance(buddy_list,list):
            buddy_list=list(buddy_list)
        for buddy in buddy_list:
            try:
                self.api.create_friendship(buddy)
            except:
                logging.warning("{} didn't find this buddy: {} \n".format(self.name,buddy))

    def search_and_retweet(self, buddy_list, hash_list):
        self.logger.debug("search_and_retweet")
        if not isinstance(hash_list,list):
            hash_list=list(hash_list)
        for tag in hash_list:
            if random.random() > 0.7:
                hash_cursor = tweepy.Cursor(self.api.search, q="#"+tag).items()
                for tweet in hash_cursor:
                    if random.random() > 0.7:
                        self.api.retweet(tweet.id)
            # cursor=tweepy.Cursor("c", id=user, count=5000).pages()

    def search_and_follow(self, buddy_list, hash_list):
        self.logger.debug("search_and_follow")
        if not isinstance(hash_list,list):
            hash_list=list(hash_list)
        for tag in hash_list:
            if random.random() > 0.7:
                hash_cursor = tweepy.Cursor(self.api.search, q="#"+tag).items()
                for tweet in hash_cursor:
                    if random.random() > 0.8:
                        self.api.create_friendship(tweet.author.id)

    def retweet_my_friends(self, buddy_list, hash_list):
        self.logger.debug("retweet_my_friends")
        if not isinstance(buddy_list, list):
            buddy_list=list(buddy_list)
        random.shuffle(buddy_list)
        for buddy in buddy_list:
            try:
                tweets = self.api.user_timeline(screen_name=buddy)
                #self.stream.filter(buddy, _with='followings', async = True)
            except:
                logging.warning("user {} timeline not accesible \n".format(buddy))
                for tweet in tweets:
                    if random.random()>0.8:
                        self.api.retweet(tweet.id)

    #This function obtain tweet for the indicated query,
    #it will save into db untill the element get the willed value-count.
    #in order to start from last saved tweet after a possible break,
    #it uses the external parameters lastid, wich is obtained from db itself in runtime

#     def save_tweets(self,db,query,api=None,count=5000,lastid=0):
        # api=self.api
        # try:
            # while db.count() <count:
                # cursor=api[0].search(q=query,since_id=lastid)
                # for tweet in cursor:
    # #some information will be saved, this isn't complete but exahustive
                    # db.insert({"status":{"author_name":tweet.author.name,\
                                # "author_id":tweet.author.id,\
                                # "author_json":tweet.author._json,\
                                # "status_json":tweet._json}\
                                # })
                    # lastid=tweet.id
            # return lastid
        # except:
            # return lastid

    #this function returns all elements already "scrapied", that is which followers already are in userdb.
    #this is to restart program since any lose too.
    # def scrapied (self,userdb=None):
        # userdb=self.userdb
        # for i in userdb.find():
            # yield int(i['user'].keys()[0])

    # #a simple rotate function very usefull for api index scrolling
    # def rotate(self,l):
        # return l[1:] + l[:1]

    # #it parses tweetsdb and return all authors, obviously the db is parsed only at first instance,
    # #then everything is saved to user_list, and authors popped from there.
    # #

    # def get_users(self, tweetsdb, last_user=0, user_list=False):
        # tweetsdb=self.tweetsdb
        # if user_list:
    # #pop an item from list and return it
            # user_list.pop(0)
            # return user_list
        # else:
            # users=[int(str(user['status']['author_id']).strip()) for user in tweetsdb.find()]
            # user_list=sorted(set(users),reverse=True)[last_user:]
    # #don't reapeat user
            # for user in scrapied(userdb):
                # try:
                    # user_list.remove(user)
                # except:
                    # continue
            # return user_list

    # #most difficult to write down!
    # #this function return followers for each author, adopting some tricks to keep memory of cursor
    # #and same time get a new api when apiratelimit is exceeded
    # # def get_followers(self,user,api=none):
        # # api=self.api
        # # followers=[]
        # # count=1
        # # cursor=tweepy.cursor(api[0].followers_ids, id=user, count=5000).pages()
        # # while true:
            # # try:
                # # for page in cursor:
                    # # followers.extend(page)
                    # # print "page", count, "of user", user
                    # # sys.stdout.flush()
                    # # count +=1
                # # return followers

            # # except tweepy.ratelimiterror:
    # #new api in case is at zero page retrieved
                # # if cursor.next_cursor==-1:
                    # # self.rotate(self.api)
                    # # self.get_followers(user)
                # # else:
                    # # print "let's take a break, it will restart                        from last page; api_index is", api[0],"current cursor", cursor.next_cursor
                    # # sys.stdout.flush()
                    # # for i in range(15):
                        # # print 15-i, "minutes to wait"
                        # # time.sleep(60)
                    # # continue
            # # except:
                # # print "Unexpected!!! on user", user
                # # self.ERROR.append(user)
                # # break

    # #this function is a kind of main, retrieve users and scrapies followers for each one, then pop user and reapeat.
    # def followers(self,api=None,userdb=None,tweetsdb=None):
        # api=self.api
        # tweetsdb=self.tweetsdb
        # userdb=self.userdb
        # user_list=get_users(tweetsdb)
        # while user_list:
            # if api[0].rate_limit_status()['resources']['followers']['/followers/ids']['remaining'] <1:
                # api=self.rotate(api)
                # print ("api_index has incremented")

            # user=user_list[0]
            # followers =self.get_followers(user,api=api)
            # userdb.insert({"user":{str(user):followers}})
            # user_list=get_users(tweetsdb,user_list=user_list)




# # In[26]:

# #lastid=int(tweetsdb.find()[len([tweetsdb.find()])-1]['status']['status_json']['id_str'])


# # In[33]:

# #len(list(scrapied(userdb)))


# # In[35]:

# #len(get_users(tweetsdb))


# # In[ ]:
# '''
# lastid=int(tweetsdb.find()[len([tweetsdb.find()])-1]['status']['status_json']['id_str'])
# count=10000
# #keep it running until count
# while tweetsdb.count() < count:
    # api_index=0
    # lastid=get_tweets(db=tweetsdb,api=api,query="Daesh",count=count,lastid=lastid,api_index=api_index)
    # rotate(api)
    # print tweetsdb.count()
    # time.sleep(60*15)

# if len(get_users(tweetsdb)):
    # followers(api=api,userdb=userdb,tweetsdb=tweetsdb)
   # '''


# # In[9]:




# # In[8]:




# # In[34]:


# # In[84]:
