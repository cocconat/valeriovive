
# coding: utf-8

# In[ ]:

import tweepy, time,sys
from tweepy import OAuthHandler
import networkx as nx
import matplotlib.pyplot as plt
import tweepy.streaming 
from tweepy import StreamListener
import sys
from pymongo import MongoClient


class Tweet_clt():
    def __init__(self):
        cfgs=[]
        cfgs.append({
                "consumer_key":"Mh9rcdJ4B6YysSAi0KTDQFsM1",
                "consumer_set":"jnnaaj8pCQiGaueKNI1XXzeYTXxCJEdWRxwMA7K0DrmX3IayKr",
                "access_token":"4217826401-OFPynlsQ82cige27qxGtHNcfRlT7iBqRv3Sk2JN",
                "secret_token":"4p1r5I6gICElZdAih31OXus3xxcEDtdgh4ZiVLzl127f3"
        })

        cfgs.append({
                "consumer_key":"Gaqdl4FMffENS5mUxqYFKRORq",
                "consumer_set":"7hAz97Yp5Y8FRFykBtwMzLP7thkJ6mZCKWFEKuq8OiiDHAaqPi",
                "access_token":"4502462727-SYL1Pf8ojKLzvo4oLGQRhOLmE2qFsLwmjJVORfK",
                "secret_token":"fRALOwADcaovuXQC6M8JwiNiFhdFg14adeYYFFP1uGfF8"
        })
        cfgs.append({
                "consumer_key":"oqyXkQAJbiOAAPd4x0GBryrc2",
                "consumer_set":"ovcyD2rO9u9v5tUJ3e4RL6yoBG43GC0zDrjoLCRnsOsLk7Ny2A",
                "access_token":"4562054728-NmUimPKKacGE3gKlS7oJ3i6zSQAq2Lj347xh9Io",
                "secret_token":"6u51GoRmogD5aVZHDba0xdEi2xFricKxWZLPezPQrbwOe"
        })
        self.__cfgs=cfgs
        self.api=None
        self.userdb=None
        self.tweetsdb=None
        self.api=self.authenticate(self.__cfgs)
        self.db_instance()
        self.ERROR=[]
 
    ##Authenticate 3 twitter app as a list, the object will rotate for accelerate the download,
    #as it's done can be easily increased number of api

    def authenticate(self,cfgs):
        api=[]
        for cfg in cfgs:
            auth=OAuthHandler(cfg["consumer_key"],cfg["consumer_set"])
            auth.set_access_token(cfg["access_token"],cfg["secret_token"])
            api.append(tweepy.API(auth))
        return api
   

    #instanciate the database, a dictionary type has been choosen
    #tweetsdb will cotain the whole tweet
    #userdb will contain tweets's authors and relative followers
    def db_instance(self):
        client=MongoClient('localhost', 27017)
        if client.test_database:
            db=client.get_database('dict')
            self.userdb=db['user']
            self.tweetsdb=db['tweeets']
            #error list it's for those user resulting missing to followers retrieve
        else: raise  

    #This function obtain tweet for the indicated query, 
    #it will save into db untill the element get the willed value-count.
    #in order to start from last saved tweet after a possible break,
    #it uses the external parameters lastid, wich is obtained from db itself in runtime

    def get_tweets(self,db,query,api=None,count=5000,lastid=0):
        api=self.api
        try:
            while db.count() <count:
                cursor=api[0].search(q=query,since_id=lastid)
                for tweet in cursor:
    #some information will be saved, this isn't complete but exahustive
                    db.insert({"status":{"author_name":tweet.author.name,\
                                "author_id":tweet.author.id,\
                                "author_json":tweet.author._json,\
                                "status_json":tweet._json}\
                                })
                    lastid=tweet.id
            return lastid
        except:
            return lastid

    #this function returns all elements already "scrapied", that is which followers already are in userdb.
    #this is to restart program since any lose too.
    def scrapied (self,userdb=None):
        userdb=self.userdb
        for i in userdb.find():
            yield int(i['user'].keys()[0])
            
    #a simple rotate function very usefull for api index scrolling
    def rotate(self,l):
        return l[1:] + l[:1]

    #it parses tweetsdb and return all authors, obviously the db is parsed only at first instance,
    #then everything is saved to user_list, and authors popped from there.
    #

    def get_users(self, tweetsdb, last_user=0, user_list=False):
        tweetsdb=self.tweetsdb
        if user_list:
    #pop an item from list and return it
            user_list.pop(0)
            return user_list
        else:
            users=[int(str(user['status']['author_id']).strip()) for user in tweetsdb.find()]
            user_list=sorted(set(users),reverse=True)[last_user:]
    #don't reapeat user
            for user in scrapied(userdb):
                try:
                    user_list.remove(user)
                except:
                    continue        
            return user_list
        
    #most difficult to write down!
    #this function return followers for each author, adopting some tricks to keep memory of cursor
    #and same time get a new api when apiratelimit is exceeded
    def get_followers(self,user,api=None):
        api=self.api
        followers=[]
        count=1
        cursor=tweepy.Cursor(api[0].followers_ids, id=user, count=5000).pages()
        while True:
            try:
                for page in cursor:
                    followers.extend(page)
                    print "page", count, "of user", user
                    sys.stdout.flush()
                    count +=1
                return followers
                    
            except tweepy.RateLimitError:
    #new api in case is at zero page retrieved
                if cursor.next_cursor==-1:
                    self.rotate(self.api)
                    self.get_followers(user)
                else:
                    print "let's take a break, it will restart                        from last page; api_index is", api[0],"current cursor", cursor.next_cursor
                    sys.stdout.flush()
                    for i in range(15):
                        print 15-i, "minutes to wait"
                        time.sleep(60)
                    continue
            except:
                print "Unexpected!!! on user", user
                self.ERROR.append(user)
                break

    #this function is a kind of main, retrieve users and scrapies followers for each one, then pop user and reapeat.
    def followers(self,api=None,userdb=None,tweetsdb=None):
        api=self.api
        tweetsdb=self.tweetsdb
        userdb=self.userdb
        user_list=get_users(tweetsdb)
        while user_list:
            if api[0].rate_limit_status()['resources']['followers']['/followers/ids']['remaining'] <1: 
                api=self.rotate(api)
                print "api_index has incremented"
              
            user=user_list[0]
            followers =self.get_followers(user,api=api)
            userdb.insert({"user":{str(user):followers}})
            user_list=get_users(tweetsdb,user_list=user_list)

            


# In[26]:

#lastid=int(tweetsdb.find()[len([tweetsdb.find()])-1]['status']['status_json']['id_str'])


# In[33]:

#len(list(scrapied(userdb)))


# In[35]:

#len(get_users(tweetsdb))


# In[ ]:
'''
lastid=int(tweetsdb.find()[len([tweetsdb.find()])-1]['status']['status_json']['id_str'])
count=10000
#keep it running until count 
while tweetsdb.count() < count:
    api_index=0
    lastid=get_tweets(db=tweetsdb,api=api,query="Daesh",count=count,lastid=lastid,api_index=api_index)
    rotate(api)
    print tweetsdb.count()
    time.sleep(60*15)

if len(get_users(tweetsdb)):
    followers(api=api,userdb=userdb,tweetsdb=tweetsdb)
   '''         


# In[9]:




# In[8]:




# In[34]:


# In[84]:
