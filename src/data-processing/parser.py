from twitterscraper import query_tweets

def query(subject, since, until, near = None, limit = None):
    """
    Returns tweets matching parameters

    :param subject: subject of tweet ("Trump OR Nagi") 
    :param since: fetch tweets since that date ("2017-11-30")
    :param until: fetch tweets until that date ("2017-12-24")
    :param near: fetch tweets published near that location ("New York")
    :param limit: minimum number of tweets to fetch ("1000")

    :return tweets: tweets that match description
    :rtype: list<Tweet>
    """
    query = ""
    query += subject
    if near is not None:
        query += " near:" + near
    query += " since:" + since
    query += " until:" + until
    
    return query_tweets(query, limit)
        
def save_query(filename, subject, since, until, near = None, limit = None):
    """
    Fetch tweets matching description and save them into file

    
    """
    file = open(filename, "w")
    for tweet in query(subject, since, until, near, limit):
        file.write(tweet.encode('utf-8'))
    file.close()

