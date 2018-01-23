import os, errno

try:
    import json
except ImportError:
    import simplejson as json

from twitterscraper import query_tweets
import datetime
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

    since_date = datetime.datetime.strptime(since, '%Y-%m-%d')
    since_date += datetime.timedelta(days=-1)
    until_date = datetime.datetime.strptime(until, '%Y-%m-%d')
    until_date += datetime.timedelta(days=1)
    since = since_date.strftime('%Y-%m-%d')
    until = until_date.strftime('%Y-%m-%d')
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
    print(query)
    return query_tweets(query, limit)

def fetch_and_save_tweets(filename, subject, since, until, near = None, limit = None):
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
    limit = int(limit)
    if near is not None:
        near = near.lower()
    filename = '.cache/' + subject + '_' + near + '.json'
    if not(os.path.isdir('.cache')):
        os.makedirs('.cache/')

    since_date = datetime.datetime.strptime(since, '%Y-%m-%d')
    until_date = datetime.datetime.strptime(until, '%Y-%m-%d')
    if since_date > until_date :
       tmp_date = since_date
       since_date = until_date
       until_date = tmp_date
       tmp = since
       since = until
       until = tmp
    since_date1 = since_date
    until_date1 = until_date
    since_date_double = None
    until_date_double = None

    since_json = since
    until_json = until

    # main JSON to save in cache
    data = {}
    tweets = []
    do_fetch = True
    between = False
    json_tweets = []
    # Remove file with same filename if exists
    if os.path.isfile(filename) :
        json_file = open(filename, 'r')
        json_data = json.load(json_file)
        since2 = json_data['query']['since']
        since_date2 = datetime.datetime.strptime(since2, '%Y-%m-%d')
        until2 = json_data['query']['until']
        until_date2 = datetime.datetime.strptime(until2, '%Y-%m-%d')

        json_tweets = json_data['tweets']
        json_tweets.reverse()
        print(str(len(json_tweets)) + ' tweets in cache for this query')
        if until_date <= until_date2 and until_date >= since_date2 :
            between = True
            count = 0
            for tweet in json_tweets :
                timestamp = tweet['timestamp']
                date_time = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                if date_time < since_date :
                    break
                if date_time < until_date :
                    if count < limit :
                        tweets.append(tweet)
                        count += 1
                    else :
                        do_fetch = False
                        break
            until_date1 = since_date2
            until_date1 += datetime.timedelta(days=-1)
            until_json = until2
            limit = limit - count
            print('(1) Loaded ' + str(count) + ' tweets from cache')
        if since_date <= until_date2 and since_date >= since_date2 :
            between = True
            since_date1 = until_date2
            since_json = since2
        if not between :
            if until_date < since_date2 :
                since_json = since
            elif since_date > until_date2 :
                until_json = until
            else :
                since_date_double = since_date

    if until_date1 < since_date1 :
        do_fetch = False
        print('- Unnecessary to fetch -')
        return tweets

    since = since_date1.strftime('%Y-%m-%d')
    until = until_date1.strftime('%Y-%m-%d')

    #try:
    #    os.remove(filename)
    #except OSError as e:
    #    if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
    #        raise

    # save query into JSON
    query = {}
    query['subject'] = subject
    query['near'] = near
    query['since'] = since_json
    query['until'] = until_json
    # add JSON query to main JSON
    data['query'] = query

    to_save = []
    # fetch tweets and add them to dic
    query_tweets = fetch_tweets(subject, since, until, near, limit)
    query_tweets.reverse()
    print('Downloaded ' + str(len(query_tweets)) + ' new tweets')
    fetched_tweets = []
    for tweet in query_tweets:
        t = {}
        t['text'] = tweet.text
        t['timestamp'] = str(tweet.timestamp)
        fetched_tweets.append(t)
    if not tweets :
        to_save.extend(fetched_tweets)
        to_save.extend(json_tweets)
    else :
        to_save.extend(json_tweets)
        to_save.extend(fetched_tweets)
    tweets.extend(fetched_tweets)
    if between :
        count = len(tweets)
        i = 0
        for tweet in json_tweets :
            timestamp = tweet['timestamp']
            date_time = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            if date_time < since_date :
                break
            if date_time < until_date :
                if count < limit :
                    tweets.append(tweet)
                    count += 1
                    i += 1
                else :
                    break
        print('(2) Loaded ' + str(i) + ' tweets from cache')

    to_save.reverse()
    data['tweets'] = to_save
    
    # save tweets into file as json
    file = open(filename, 'w')
    file.write(json.dumps(data))
    file.close()

    return tweets

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

def save_tweets_2_file(tweets, f):
    """
    writing tweets in a file f given

    Params:
        :tweets -- list(tweet) : list of the tweets
        :f -- file :  file where to write tweets
    """
    data = {}
    data['tweets'] =  [tweet.text for tweet in tweets]
    text2save =  json.dumps(data)
    f.write(text2save)

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
