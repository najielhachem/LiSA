from twitter import *
try:
    import json
except ImportError:
    import simplejson as json
import time
import shutil
import os

ACCESS_TOKEN = '878150818553364481-e5FF1neZRRO1w2TbyH5L9USloCbePqM'
ACCESS_SECRET = 'CTirUNzwfZYSvnKksyBCoRQlDuepKFyxNPaKaD9xeo5dW'
CONSUMER_KEY = 'ktqbQBV0ObLrLvdg8fla9LxMW'
CONSUMER_SECRET = 'NHHIxsH85llQCtKB0LKAJ7LxUSjNSIdznkkgdewbVHHFYvAXd6'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter = Twitter(auth = oauth)


class Request:
    def __init__(self):
        self.request_count = 0


    def getFriendList(self, name):
        if (self.request_count >= 180):
            print("Sleeping 15min")
            time.sleep(900)
        return twitter.friends.list(screen_name=name, count=200)


    def getFriendsCount(self, name, d):
        score = 1

        if d > 0:
            friendList = getFriendList(name)
            for friend in friendList["users"]:
                score += getFriendsCount(friend["screen_name"], d-1)

        return score


    def getTweets(self, name):
        results = twitter.search.tweets(q = name, count=150)
        return results["statuses"]

directory = "parsing"
if os.path.exists(directory):
    shutil.rmtree(directory)
os.makedirs(directory)
req = Request()
for e in req.getFriendList('EmmanuelMacron')['users']:
    tweets = req.getTweets(e["screen_name"])
    f = open("parsing/" + e["screen_name"], "w")
    for t in tweets:
        f.write(t["text"] + "\n\n")
    f.close()
