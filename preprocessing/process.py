import numpy as np
import csv
import re
from textblob import TextBlob
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer

def getData(path):
    f = open(path, "r")
    l = list(csv.reader(f))
    n = len(l)
    for i in range(n):
        l[i] = np.array([l[i][1],process(l[i][3])])
    l = np.array(l)
    cond = l[:, 1] != "__DELETE"
    l = l[cond] 
    return l

# Hashtags
hash_regex = re.compile(r"#(\w+)")

def hash_repl(match):
    return '__HASH_' + match.group(1).upper()

# Repeating words like hurrrryyyyyy
rpt_regex = re.compile(r"(.)\1{1,}", re.IGNORECASE);

def rpt_repl(match):
    return match.group(1) + match.group(1)

# Emoticons
emoticons = [ \
        ('__EMOT_SMILEY', [':-)', ':)', '(:', '(-:']), \
        ('__EMOT_LAUGH', [':-D', ':D', 'X-D', 'XD', 'xD']), \
        ('__EMOT_LOVE',	['<3', ':\*']), \
        ('__EMOT_WINK',	[';-)', ';)', ';-D', ';D', '(;', '(-;']), \
        ('__EMOT_FROWN', [':-(', ':(', '(:', '(-:']), \
        ('__EMOT_CRY', [':,(', ':\'(', ':"(', ':((']), \
        ]

def escape_paren(arr):
    return [text.replace(')', '[)}\]]').replace('(', '[({\[]') for text in arr]

def regex_union(arr):
    return '(' + '|'.join( arr ) + ')'

emoticons_regex = [ \
        (repl, re.compile(regex_union(escape_paren(regx)))) \
        for (repl, regx) in emoticons \
        ]


# Hashtags
hash_regex = re.compile(r"#(\w+)")

def hash_repl(match):
    return '__HASH_' + match.group(1).upper()

# URLs
url_regex = re.compile(r"(http|https|ftp)://[a-zA-Z0-9\./]+|www.[a-zA-Z0-9\./]+")

# Determinants
det_regex = re.compile(r"the|of|and|my|yours|to|your|his|its|our|their|these|this|those|what|which|whose|her")

# Retweets
rt_regex = re.compile(r".*\sRT\b")

def processDeterminants(text):
    return re.sub(det_regex, "", text)

def processHashtags(text):
    return re.sub(hash_regex, hash_repl, text)

def processUrls(text):
    return re.sub(url_regex, "__URL", text)

def processRepeatLetters(text):
    return re.sub(rpt_regex, rpt_repl, text)

def processEmoticons(text, remove_emoticon):
    for (repl, regx) in emoticons_regex:
        if remove_emoticon:
            text = re.sub(regx, '', text)
    else:
        text = re.sub(regx, ' ' + repl + ' ', text)
    return text

def processRetweets(text):
    m = rt_regex.match(text)
    if (m):
        return "__DELETE"
    else: 
        return text

def processSteamLeam(text):
    stem = LancasterStemmer()
    lem = WordNetLemmatizer()
    l = re.split(",| ", text)
    l = np.array([stem.stem(lem.lemmatize(l[i])) for i in range(len(l))])
    text = " ".join(l)
    return text

def processTextBlob(text):
    text = TextBlob(text)
    if (text.detect_language() != 'en'):
        return "__DELETE"
    #text = text.correct()
    lstr = text.words.singularize()
    lstr = lstr.lemmatize()
    return " ".join(lstr)

def process(text, remove_emoticon = True):
    text = processRepeatLetters(text)
    #print("Repeated ",text)
    text = processUrls(text)
    #print("Urls",text)
    text = processEmoticons(text, remove_emoticon)
    #print("Emoticons",text)
    text = processDeterminants(text)
    #print("Determinants",text)
    text = processRetweets(text)
    #print("Retweets",text)
    #text = processTextBlob(text)
    #print("TextBlob",text)
    text = processSteamLeam(text)
    return text

