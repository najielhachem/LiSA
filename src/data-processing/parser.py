from twitterscraper import query_tweets

def query(subject, since, until, near = None, limit = None):
    query = subject
    if near is not None:
        query += " near:" + near
    query += " since:" + since
    query += " until:" + until
    
    return query_tweets(query, limit)
        
def save_query(filename, subject, since, until, near = None, limit = None):
    file = open(filename, "w")
    for tweet in query(subject, since, until, near, limit):
        file.write(tweet.encode('utf-8'))
    file.close()

