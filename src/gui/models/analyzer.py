from .classifiers import *
import data_processing.preprocessor as preprocessor
import data_processing.parser as parser
import math
import sklearn.feature_extraction.text as skl_txt

import numpy as np

import time
import pickle

class Analyzer:
    def __init__(self, classifier = LinearSVC()):
        self.classifier = classifier
        self.vectorizer = None
        self.tweets = []

    def set_tweets(self, tweets):
        self.tweets = tweets
    def get_tweets(self):
        return self.tweets

    def analyze(self):
        """ using defined classifier, value between 0 and 1
            Args:
                tweet_texts ([string]): Array of string corresponding to tweets
        """
        processor = preprocessor.Preprocessor()
        tweets_text = [processor.default_processing(tweet.text) for tweet in self.tweets]
        tweets_text = self.vectorize_data(tweets_text)
        try:
            self.labels = self.classifier.predict(tweets_text)
            print(self.labels)
        except:
            self.classifier.load()
            self.labels = self.classifier.predict(tweets_text)

    def segment_labels(self, period, start, end):
        """
            Return list of tweets segmented by the attribute timestamp on [nb_segments - 1] interval
        Params :
            :period -- period in seconds
        """
        total_period = (end - start)
        nb_segments = math.ceil(total_period / period)
        segmented_labels = np.empty(nb_segments)
        for segment in range(nb_segments):
            label = 0
            nb_tweets = 0
            for i, tweet in enumerate(self.tweets):
                tweet_time = tweet.__getattribute__('timestamp')
                tweet_time = time.mktime(tweet_time.timetuple()) # transform to seconds
                if (segment * period + start ) <= tweet_time and tweet_time < ((segment + 1) * period + start):
                    if self.labels[i] == 1:
                        label += 1
                    else:
                        label -= 1
                    nb_tweets += 1
            if nb_tweets == 0:
                label = -2
            else:
                label = label / nb_tweets
            segmented_labels[segment] = label
        return segmented_labels

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

    def __load_vectorizer(self, path='data/objects/vectorizers/tfidf'):
        try:
            with open(path, "rb") as file:
                self.vectorizer = pickle.loads(b''.join(file.readlines()))
        except:
            print("This vectorizer does not exist.")

    def vectorize_data(self, text_data):
        if self.vectorizer is None:
            self.__load_vectorizer()
        return self.vectorizer.transform(text_data)
