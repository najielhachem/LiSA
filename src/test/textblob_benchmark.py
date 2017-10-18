from textblob import TextBlob
import sys
import re

def clean_tweet(tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(clean_tweet(tweet))
        # set sentiment
        return analysis.sentiment.polarity
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

def getDataLines(file_path):
    f = open(file_path, "r")
    lines = f.readlines()
    f.close
    return lines

def main(argv=None):
    if (argv is None):
        argv = sys.argv

    lines = getDataLines(argv[1])
    count  = 0
    acc = 0
    for l in lines[1:]:
        l = l.split(",")
        feeling = get_tweet_sentiment(l[3])
        if (feeling != 0):
            count = count + 1
            if (feeling > 0 and int(l[1]) == 1) or (feeling < 0 and int(l[1]) == 0):
                acc = acc + 1
    print(acc/count)

if __name__ == '__main__':
    main()
