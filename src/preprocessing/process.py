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


def get_language_likelihood(input_text):
    """Return a dictionary of languages and their likelihood of being the 
    natural language of the input text
    """
 
    input_text = input_text.lower()
    input_words = wordpunct_tokenize(input_text)
 
    language_likelihood = {}
    total_matches = 0
    for language in stopwords._fileids:
        language_likelihood[language] = len(set(input_words) &
                set(stopwords.words(language)))
 
    return language_likelihood
 
def get_language(input_text):
    """Return the most likely language of the given text
    """
    likelihoods = get_language_likelihood(input_text)
    return sorted(likelihoods, key=likelihoods.get, reverse=True)[0]
 
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



# Determinants
det_regex = re.compile(r"the|of|and|my|yours|to|your|his|its|our|their|these|this|those|what|which|whose|her")

# Retweets
rt_regex = re.compile(r".*\sRT\b")

def process_determinants(text):
    return re.sub(det_regex, "", text)

def process_hashtags(text):
    return re.sub(hash_regex, hash_repl, text)

def process_urls(text):
    # URLs
    url_regex = re.compile(r"(http|https|ftp)://[a-zA-Z0-9\./]+|www.[a-zA-Z0-9\./]+")
    return re.sub(url_regex, "__URL", text)

def process_repeated_letters(text):
    return re.sub(rpt_regex, rpt_repl, text)

def process_emoticons(text, remove_emoticon):
    for (repl, regx) in emoticons_regex:
        if remove_emoticon:
            text = re.sub(regx, '', text)
        else:
            text = re.sub(regx, ' ' + repl + ' ', text)
    return text

def process_retweets(text):
    m = rt_regex.match(text)
    if (m):
        return "__DELETE"
    else: 
        return text
    
def process_lematize(text):
    lem = WordNetLemmatizer()
    words = text.split(" ")
    words = np.array([lem.lemmatize(word) for word in words])
    text = " ".join(words)
    return text

def process_stem(text):
    stem = LancasterStemmer()
    words = text.split(" ")
    words = np.array([stem.stem(word) for word in words])
    text = " ".join(words)
    return text

def process_TextBlob(text):
    text = TextBlob(text)
    if (text.detect_language() != 'en'):
        return "__DELETE"
    lstr = text.words.singularize()
    lstr = lstr.lemmatize()
    return " ".join(lstr)

def process_language(text):
    if(get_language(text) != 'english'):
        return "__DELETE"
    return text

def process_ponctuation(text):
    ponctuation = "\n\t!?<>:,;.()[]{}\\/_&\"'-=+*"
    for p in ponctuation:
        text = text.replace(p, ' ')
    text = text.split(' ')
    text = list(filter(lambda a: a != '', doc))
    return np.array(text)

def process(text, remove_emoticon = False):
    text = process_ponctuation(text)
    text = process_repeated_letters(text)
    text = process_urls(text)
    text = process_emoticons(text, remove_emoticon)
    text = process_determinants(text)
    text = process_retweets(text)
    text = process_lematize(text)
    return text

