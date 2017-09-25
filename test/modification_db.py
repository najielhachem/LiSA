import sys
import nltk
import numpy as np
import json
import ast


NB_OF_WORD = 2000

def getDataLines(file_path):
    f = open(file_path, "r")
    lines = f.readlines()
    f.close
    return lines

def save_lemmatized_db(lines):
    f = open("db_leming.csv", "w")
    for l in lines[1:10]:
        l = l.split(",")
        ll = nltk.word_tokenize(l[3])
        a = {}
        a[l[1]] = str(ll)
        f.write(json.dumps(a) + "\n")
    f.close
    return "db_leming.csv"

def get_word_count(lemmatized_db_file):
    f = open(lemmatized_db_file, "r")
    d = {}
    for l in f:
        for j in json.loads(l).items():
            for e in ast.literal_eval(j[1]):
                if e not in d:
                    d[e] = 1
                else:
                    d[e] = d[e] + 1
    d = [(w, d[w]) for w in sorted(d, key=d.__getitem__, reverse = True)]
    f.close
    return d

def save_most_fq_word(d):
    f = open("most_fq_words.csv", "w")
    for e in (d[:NB_OF_WORD] if len(d) > NB_OF_WORD else d):
        f.write(str(e) + "\n")
    f.close()
    return "most_fq_words.csv"

def get_base(file):
    f = open(file, "r")
    b = []
    for l in f:
        b.append(ast.literal_eval(l)[0])
    return b

def get_lem_tweets(file):
    f = open(file, "r")
    t = []
    for l in f:
        d = ast.literal_eval(l)
        for e in d:
            t.append([e, ast.literal_eval(d[e])])
    return t

def get_vectors(lem_tweets, base):
    vect = []
    for t in lem_tweets:
        v = []
        for w in base:
            if w in t[1]:
                v.append(1)
            else:
                v.append(0)
        vect.append((t[0], v))
    return vect


def main(argv=None):
    if (argv is None):
        argv = sys.argv

    lines = getDataLines(argv[1])
    lemmatized_db_file = save_lemmatized_db(lines)
    d = get_word_count(lemmatized_db_file)
    base_path = save_most_fq_word(d)
    base = get_base(base_path)
    lem_tweets = get_lem_tweets(lemmatized_db_file)
    vects = get_vectors(lem_tweets, base)
    #for v in vects:
    #    print(v)

if __name__ == '__main__':
    main()
