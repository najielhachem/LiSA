from .classifiers import *
import data_processing.preprocessor as preprocessor
from data_processing.parser as parser
import numpy as np
import math
import sklearn.feature_extraction.text as skl_txt

class Analyzer:
    def __init__(self, classifier = LinearSVC()):
        self.classifier =classifier



    def set_tweets(self, tweets):
        self.tweets = tweets

    def analyze(self):
        """ using defined classifier, value between 0 and 1
            Args:
                tweet_texts ([string]): Array of string corresponding to tweets
        """
        processor = preprocessor.Preprocessor()
        tweets_text = [processor.default_processing(tweet.text) for tweet in self.tweets]
        tweets_text = self.vectorize_data(tweets_text)
        self.labels = self.classifier.predict(tweets_text)

    def segment_labels(self, period, start, end):
        """
            Return list of tweets segmented by the attribute timestamp on [nb_segments - 1] interval
        Params :
            :period -- period in seconds
        """
        total_period = (end - start)
        nb_segments = math.ceil(total_period / period)
        segemented_labels = [
                [ self.labels[j]
                    for j in range(self.tweets)
                    if (i * period + start ) <= self.tweets[j].__getattribute__('timestamp')
                    and self.tweets[j].__getattribute__('timestamp') < ((i + 1) * period + start)
                ] for i in range(nb_segments) ]
        return np.array(segemented_labels)

    def segment_tweets_nb_segments(self, nb_segments):
        """
            Return list of tweets segmented by the attribute timestamp on [nb_segments - 1] interval
        Params :
            :tweets -- list[tweet]: list of tweets done by a query
        """
        time_stamps = np.array([tweet.__getattribute__('timestamp') for tweet in self.tweets])
        time_min = time_stamps.min()
        time_max = time_stamps.max()
        total_period = time_max - time_min
        delta = datetime.timedelta(seconds = (total_period.total_seconds()/ nb_segments))
        segemented_tweets = [
                [ tweet
                    for tweet in self.tweets
                    if (i * delta + time_min ) <= t.__getattribute__('timestamp')
                    and t.__getattribute__('timestamp') < ((i + 1) * delta + time_min)
                ] for i in range(nb_segments) ]
        return np.array(segemented_tweets), total_period

    def vectorize_data(self, text_data, ngrams=(1,1), binn=False, idf=True):
        if (binn == True):
            idf = False
        vectorizer = skl_txt.TfidfVectorizer(use_idf = idf, binary = binn, ngram_range = ngrams)
        return vectorizer.fit_transform(text_data)
