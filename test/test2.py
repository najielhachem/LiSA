from twitterscraper import query_tweets
import json


# All tweets matching either Trump or Clinton will be returned. You will get at
# least 10 results within the minimal possible time/number of requests
for tweet in query_tweets("Trump OR Clinton", 10)[:10]:
    print(tweet.__dict__["user"])
