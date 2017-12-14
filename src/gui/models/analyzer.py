from .classifiers import *

class Analyzer:
    def __init__(self, classifier = BernoulliNB()):
        self.classifier = classifier

    def set_tweets(self, tweets):
        self.tweets = tweets

    def analyze(self):
        """ Return, using defined classifier, value between 0 and 1
            Args:
                tweet_texts ([string]): Array of string corresponding to tweets
        """
        return self.classifier.predict(self.tweets)

    def segment_tweets(tweets, nb_segments):
        """
            Return list of tweets segmented by the attribute timestamp on [nb_segments - 1] interval
        Params :
            :tweets -- list[tweet]: list of tweets done by a query
        """
        time_stamps = np.array([tweet[i].__getattribute__('timestamp') for i in range(len(tweets))])
        time_min = time_stamps.min()
        time_max = time_stamps.max()
        delta = datetime.timedelta(seconds = ((time_max - time_min).total_seconds()/ nb_segments))
        segemented_tweets = [[t for t in tweets
        if( (( i  * delta) + time_min ) <= t.__getattribute__('timestamp') < (( (i + 1) * delta) + time_min ) )] for i in range(nb_segments)]
        return segemented_tweets
