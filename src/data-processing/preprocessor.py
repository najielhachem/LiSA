import numpy as np

import re
import nltk 
# nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer


class Preprocessor:

    def __init__(self):
        # Determinants
        self.det_regex = re.compile(r"the|of|and|my|yours|to|your|his|its|\
                our|their|these|this|those|what|which|whose|her")
        # Hashtags
        self.hash_regex = re.compile(r"#(\w+)")
        # URLs
        self.url_regex = re.compile(r"(http|https|ftp)://[a-zA-Z0-9\./]+|\
                www.[a-zA-Z0-9\./]+")
        # Repeating words like hurrrryyyyyy
        self.rpt_regex = re.compile(r"(.)\1{1,}", re.IGNORECASE);
        # Retweet
        self.rt_regex = re.compile(r".*\sRT\b")
        # Paranthesis
        self.openning = re.compile(r"\[|\{|\(")
        self.closing = re.compile(r"\]|\}|\)")
        # Emoticons
        self.emoticons_regex = self.__init_emoticons_regex()

    def __init_emoticons_regex(self):
        emoticons = [ \
                ('__EMOT_SMILEY', [':-)', ':)', '(:', '(-:']), \
                ('__EMOT_LAUGH', [':-D', ':D', 'X-D', 'XD', 'xD']), \
                ('__EMOT_LOVE', ['<3', ':\*']), \
                ('__EMOT_WINK', [';-)', ';)', ';-D', ';D', '(;', '(-;']), \
                ('__EMOT_FROWN', [':-(', ':(', '(:', '(-:']), \
                ('__EMOT_CRY', [':,(', ':\'(', ':"(', ':((']), \
                ]
        n = len(emoticons)
        escaped_emoticons = [None] * n
        for i in range(n):
            escaped_emoticons[i] = (emoticons[i][0],
                    [emoji.replace(')', '\)').replace('(', '\(') for emoji in emoticons[i][1]])
        
        emoticons_regex = [ \
                (repl, re.compile(r"(" + "|".join(regx) + ")")) \
                for (repl, regx) in escaped_emoticons \
                ]
        return emoticons_regex


    def uniform_parenthesis(self, tweet, openning = "(", closing = ")"):
        tweet = re.sub(self.openning, openning, tweet)
        tweet = re.sub(self.closing, closing, tweet)
        return tweet

    def uniform_emoticons(self, tweet):
        for (repl, regx) in self.emoticons_regex:
            tweet = re.sub(regx, ' ' + repl + ' ', tweet)
        return tweet

    def replace_hashtags(self, tweet, tag = "__HASH__"):
        return re.sub(self.hash_regex, tag, tweet)

    def replace_urls(self, tweet, tag = "__URL__"):
        return re.sub(self.url_regex, tag, tweet)

    def is_retweet(self, tweet):
        if self.rt_regex.match(tweet):
            return True
        return False

    def remove_determinants(self, tweet):
        return re.sub(self.det_regex, "", tweet)

    def remove_repeated_letters(self, tweet):
        def __rptd_replace(match):
            return match.group(1) + match.group(1)
        return re.sub(self.rpt_regex, __rptd_replace, tweet)

    def remove_emoticons(self, tweet):
        for (repl, regx) in self.emoticons_regex:
            tweet = re.sub(regx, '', tweet)
        return tweet

    def remove_ponctuation(self, tweet):
        ponctuation = "\n\t!?<>:,;.()[]{}\\/_&\-=+*"
        for p in ponctuation:
            tweet = tweet.replace(p, ' ')
        return tweet

    def lemmatize(self, tweet):
        lem = WordNetLemmatizer()
        words = tweet.split(" ")
        words = np.array([lem.lemmatize(word) for word in words])
        tweet = " ".join(words)
        return tweet

    def default_processing(self, tweet):
        tweet = self.remove_repeated_letters(tweet)
        tweet = self.replace_urls(tweet)
        tweet = self.uniform_emoticons(tweet)
        tweet = self.uniform_parenthesis(tweet)
        tweet = self.replace_determinants(tweet)
        tweet = self.remove_retweet(tweet)
        tweet = self.lemmatize(tweet)
        tweet = self.remove_ponctuation(tweet)
        return tweet


