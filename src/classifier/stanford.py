import time
import json
import matplotlib.pyplot as plt

import numpy as np

import sklearn.feature_extraction.text as skl_txt
import sklearn.linear_model as skl_lm
import sklearn.neighbors as skl_nei
import sklearn.ensemble as skl_en
import sklearn.naive_bayes as skl_nb
import sklearn.svm as skl_svm

from sklearn import metrics as skl_metrics
import preprocessing as pre

data_dir = "../../data/data_cleaned/labelised/"
img_dir = "../../benchmarks/"

path_hutto = data_dir + "hutto.txt"
path_airline = data_dir + "airline.txt"
path_kaggle = data_dir + "kaggle.txt"
path_michigan = data_dir + "michigan.txt"
path_rtneg = data_dir + "rt-polarity-neg.txt"
path_rtpos = data_dir + "rt-polarity-pos.txt"

data_files = {
#    "hutto" : path_hutto,
    "airline" : path_airline,
    "kaggle" : path_kaggle,
#    "michigan" : path_michigan,
             }

ngrams = (1,1)
binn = False
idf = True


def parse_file(file_path):
    f = open(file_path, "r")
    file_data = json.loads(f.readlines()[0])
    f.close()
    return np.array(file_data)

def preprocess(text_data):
    for i, tweet in enumerate(text_data):
        t = pre.process(tweet, remove_emoticon=False)
        text_data[i] = t

def vectorize_data(text_data, ngrams, binn, idf):
    if (binn == True):
        idf = False
    vectorizer = skl_txt.TfidfVectorizer(use_idf = idf, binary = binn, ngram_range = ngrams)
    return vectorizer.fit_transform(text_data)

def parse_data(file_data):
    data, labels = file_data[:, 1], np.array(file_data[:, 0], dtype='int')
    preprocess(data)
    data = vectorize_data(data, ngrams, binn, idf)
    return partition_data(data, labels)

def partition_data(data, labels, ratio = 0.7):
    N = int(ratio * data.shape[0])
    idx = np.random.permutation(data.shape[0])
    train_data = data[idx[:N]]
    train_labels = labels[idx[:N]]
    test_data = data[idx[N:]]
    test_labels = labels[idx[N:]]
    return train_data, train_labels, test_data, test_labels

def get_data(files):
    data = {}
    for key in files:
        file_data = parse_file(files[key])
        tr_data, tr_labels, te_data, te_labels = parse_data(file_data)
        partitioned_data = {
            'train_data': tr_data,
            'train_labels' : tr_labels,
            'test_data': te_data,
            'test_labels' : te_labels
        }
        data[key] = partitioned_data
    return data

def get_metrics(test_labels, predicted_labels):
    acc = skl_metrics.accuracy_score(test_labels, predicted_labels)
    recall = skl_metrics.recall_score(test_labels, predicted_labels)
    pre = skl_metrics.precision_score(test_labels, predicted_labels)
    F1 = 2 * (pre * recall) / (pre + recall)
    return pre, recall, acc, F1

def validate_performance(clf, data_train, train_labels, data_test, test_labels):
    t = time.time()
    clf.fit(data_train, train_labels)
    t1 = time.time() - t
    t = time.time()
    pr_lbls = clf.predict(data_test)
    t2 = time.time() - t
    return get_metrics(test_labels, pr_lbls) + (t1, t2)

def autolabels(rects, ax, time = False):
    for rect in rects:
        height = rect.get_height()
        if (time):
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%f' % float(height) + "s",
                  ha='center', va='bottom')
        else:
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%d' % int(height * 100) + "%",
                  ha='center', va='bottom')

def plot_results(labels, results, plot_label):
    ind = np.arange(len(labels))  # the x locations for the groups

    width = 0.18    # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind , results[:,0], width, color='g')
    rects2 = ax.bar(ind - width, results[:,1], width, color='r')
    rects3 = ax.bar(ind + width, results[:,2], width, color='b')
    rects4 = ax.bar(ind + 2 * width, results[:,3], width, color='y')

    # add some text for labels, title and axes ticks
    ax.set_ylim(0,1.4)
    ax.set_ylabel('Percent')
    ax.set_title('performance on: ' + plot_label)
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(labels, rotation = 'horizontal')
    ax.legend((rects1[0], rects2[0], rects3[0], rects4[0]), ('precision', 'recall', 'accuracy', 'F1 score'), bbox_to_anchor=(1.3,1), loc="upper right")

    autolabels(rects1, ax)
    autolabels(rects2, ax)
    autolabels(rects3, ax)
    autolabels(rects4, ax)
    plt.rcParams["figure.figsize"] = [16,9]
    plt.savefig(img_dir + plot_label + "-perf.png", bbox_inches="tight")

def plot_time(labels, time_exec, plot_label):
    ind = np.arange(len(labels))  # the x locations for the groups
    width = 0.35    # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width / 2, time_exec[:, 0], width, color='b')
    rects2 = ax.bar(ind + width / 2, time_exec[:, 1], width, color='r')

    # add some text for labels, title and axes ticks
    ax.set_ylim(0, time_exec.max() * 1.2)
    ax.set_ylabel('Time (s)')
    ax.set_title('execution time on: ' + plot_label)
    ax.set_xticks(ind)
    ax.set_xticklabels(labels, rotation = 'horizontal')
    ax.legend((rects1[0], rects2[0]), ('train time', 'test time'), bbox_to_anchor=(1.3,1), loc="upper right")

    autolabels(rects1, ax, time = True)
    plt.rcParams["figure.figsize"] = [16,9]

    plt.savefig(img_dir + plot_label + "-time.png", bbox_inches="tight")

def benchmark(clfs, data, dataset_label):
    results = []
    train_data = data['train_data']
    train_labels = data['train_labels']
    test_data = data['test_data']
    test_labels = data['test_labels']
    for clf, name in clfs:
        results.append(validate_performance(clf, train_data, train_labels, test_data, test_labels))
    results = np.array(results)
    plot_results(clfs[:, 1], np.array(results[:, :4]), dataset_label)
    plot_time(clfs[:, 1], np.array(results[:, 4:]), dataset_label)
