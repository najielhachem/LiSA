import os, errno

try:
    import json
except ImportError:
    import simplejson as json

from twitterscraper import query_tweets
import numpy as np

def get_query_str(subject, since, until, near = None, limit = None):
    """
    Returns the query string that twitter scrapper accepts

    Params:
        :subject -- str: subject of tweet ("Trump OR Nagi")
        :since   -- str: fetch tweets since that date ("2017-11-30")
        :until   -- str: fetch tweets until that date ("2017-12-04")
        :near    -- str: fetch tweets published near that location ("New York")
        :limit   -- int: minimum number of tweets to fetch (1000)

    Return:
        :query -- str>: query sring
    """

    query = ""
    query += subject
    if near is not None:
        query += " near:" + near
    query += " since:" + since
    query += " until:" + until
    return query

def fetch_tweets(subject, since, until, near = None, limit = None):
    """
    Returns tweets matching parameters

    Params:
        :subject -- str: subject of tweet ("Trump OR Nagi")
        :since   -- str: fetch tweets since that date ("2017-11-30")
        :until   -- str: fetch tweets until that date ("2017-12-04")
        :near    -- str: fetch tweets published near that location ("New York")
        :limit   -- int: minimum number of tweets to fetch (1000)

    Return:
        :tweets -- list<twitterscrapper.Tweet>: tweets that match description
    """

    query = get_query_str(subject, since, until, near, limit)
    return query_tweets(query, limit)

def fetch_and_save_tweets(filename, subject, since, until, near = None, limit = None):
    #TODO save tweets as object (encode datetime)
    """
    Fetch tweets matching description and save them into file

    Params:
        :filename -- str: file path in which queries will be saved  ("output.json")
        :subject  -- str: subject of tweet ("Trump OR Nagi")
        :since    -- str: fetch tweets since that date ("2017-11-30")
        :until    -- str: fetch tweets until that date ("2017-12-04")
        :near     -- str: fetch tweets published near that location ("New York")
        :limit    -- int: minimum number of tweets to fetch (1000)

    Return:
        None
    """

    subject = subject.lower()
    if near is not None:
        near = near.lower()
    filename = '.cache/' + subject + '_' + near + '.json'
    if not(os.path.isdir('.cache')):
        os.makedirs('.cache/')
    # Remove file with same filename if exists
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise

    # main JSON to save in cache
    data = {}

    # save query into JSON
    query = {}
    query['subject'] = subject
    query['near'] = near
    query['since'] = since
    query['until'] = until
    query['limit'] = limit
    # add JSON query to main JSON
    data['query'] = query

    # fetch tweets and add them to dic
    query_tweets = fetch_tweets(subject, since, until, near, limit)
    tweets = []
    for tweet in query_tweets:
        t = {}
        t['text'] = tweet.text
        t['timestamp'] = str(tweet.timestamp)
        tweets.append(t)
    data['tweets'] = tweets
    # save tweets into file as json
    file = open(filename, 'w')
    file.write(json.dumps(data))
    file.close()
    return query_tweets

def read_json(filename):
    """
    Reads a json file and returns data as a dictionary

    Params:
        :filename -- str: file path to read from

    Return:
        :data -- dict: dictionary representing data in file
    """

    with open(filename) as file:
        lines = file.readlines()[0]
        data = json.loads(lines)
    return data
def read_json_folder(folder):
    """
    Reads a directory containing json files and returns data as a dictionary

    Params:
        :folder -- str :  folder path to read from
    """
    for root, subFolders, files in os.walk(rootdir):
        data = []
        for file in files:
            Doc = open(os.path.join(root,file), "r").readline()
            data +=  json.loads(Doc)
    return data


def read_tweets(filename):
    """
    Reads only tweets from file

    Params:
        :filename -- str: file path to read from

    Return:
        :tweets -- np.array: array containing all tweets in file
    """

    data = read_json(filename)
    return np.array(data['tweets'])
