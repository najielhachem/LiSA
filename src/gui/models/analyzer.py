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
        return classifier.predict(self.tweet)
