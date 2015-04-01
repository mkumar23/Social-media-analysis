'''
Created on Sep 10, 2014
@author: Mrinal
'''
import oauth2 as oauth
import json
from __builtin__ import str
import time

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_KEY = ""
ACCESS_SECRET = ""
screenName = "mrinalkumar23"
consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
client = oauth.Client(consumer, access_token)

def getAuthentication(C_key,C_sec,A_key,A_sec):
    global CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, client, consumer, access_token, screenName 
    CONSUMER_KEY = ""
    CONSUMER_SECRET = ""
    ACCESS_KEY = ""
    ACCESS_SECRET = ""
    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
    client = oauth.Client(consumer, access_token)
    
      
   
def getTweetsByID(id):
    allTweet = []
    timeline_endpoint = "https://api.twitter.com/1.1/statuses/user_timeline.json?user_id="+str(id)+"&count=3200"
    response, data = client.request(timeline_endpoint)
    tweets = json.loads(data)
    c = 0
    print "tweet",tweets
    with open(str(id),"w") as twt:
        
        for tweet in tweets:
            if tweet != 'errors':
                c += 1
                twt.write(getUserDetailsByID(id)+'\n')
                twt.write(tweet['text'].encode('utf-8')+'\n')
    print c
def getTweetsByScrName(id):
    allTweet = []
    timeline_endpoint = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name="+str(id)+"&count=180"
    response, data = client.request(timeline_endpoint)
    tweets = json.loads(data)
    print tweets
    c = 0
    for tweet in tweets:
        c += 1 
#         print tweet['text']
    print c
def getUserDetailsByID(id):
    timeline_endpoint = "https://api.twitter.com/1.1/users/show.json?user_id="+str(id)
    response, data = client.request(timeline_endpoint)
    info = json.loads(data)
#     if not info.has_key['error']:
    if info.has_key('name'):
        return info["name"].encode('utf8')
    return ""

def getFolloweeID(scrnName):
    timeline_endpoint = "https://api.twitter.com/1.1/friends/ids.json?cursor=-1&screen_name="+scrnName+"&count=50"
    response, data = client.request(timeline_endpoint)
    userIDs = json.loads(data)
    return userIDs

def sortWithRelevance(tweet):
    tweet.sort(key = lambda x: x[2])
    return tweet

def getTweets():
    count = 0
    getAuthentication("C_key", "C_sec", "A_key", "A_sec")
    with open("weightloss_2013-08-01_2013-08-15_userids.tsv","r") as userIds:
        for id in userIds:
            getTweetsByID(int(id))
            count += 1
            if count == 20:
                break
#             time.sleep(920)

