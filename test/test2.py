from twitterscraper import query_tweets

for tweet in query_tweets("Bitcoin", 10):
    print(tweet.__dict__["text"])
    print("======")
