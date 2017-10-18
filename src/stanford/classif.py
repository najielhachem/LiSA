from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import numpy as np
import process as p

'''
def classifier_acc(clf, data_train, train_labels, data_test, test_labels, bigrams = False, binn = False, idf = True):
  # Counter word
  count_vect = CountVectorizer()
  X_train_counts = count_vect.fit_transform(data_train) 
  tfidf_transformer = TfidfTransformer()
  X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
  X_new_counts = count_vect.transform(data_test)
  X_new_tfidf = tfidf_transformer.transform(X_new_counts)
  clf.fit(X_train_tfidf,train_labels)
  predicted = clf.predict(X_new_tfidf)
  acc = (np.mean(predicted == test_labels)) 
  print(acc)
  return acc
'''
def getmyData(filepath):
  l = p.getData(filepath)
  l = l[1:10000]
  np.random.shuffle(l)
  lgt = len(l)
  ltrain = l[:int(lgt * 0.8)]
  ltest = l[int(lgt * 0.8):]
  Y_train = ltrain[:,0]
  Y_train = np.array([int(e) for e in Y_train])
  X_train = ltrain[:,1]
  Y_test = ltest[:,0]
  Y_test = np.array([int(e) for e in Y_test])
  X_test = ltest[:,1]
  return (X_train, Y_train,X_test,Y_test)


def classify(clf, data_train, train_labels, data_test, test_labels, bigrams = False, binn = False, idf = True):
  vec = TfidfVectorizer(use_idf = idf, binary = False, )
  X_train_tfidf = vec.fit_transform(data_train) 
  X_test_tfidf =  vec.transform(data_test)
  clf.fit(X_train_tfidf,train_labels)
  predicted = clf.predict(X_test_tfidf)

  #print(pred)
  #print(test_labels)
  acc = metrics.accuracy_score(test_labels, predicted)
  recall = metrics.recall_score(test_labels, predicted)
  pre = metrics.precision_score(test_labels, predicted)
  #av_pre = 0 
  #return (av_pre, recall, acc)
  return (pre, recall, acc)

def bench():
  clf = MultinomialNB()
  filepath = 'file2.csv'
  X_tr,Y_tr,X_te,Y_te = getmyData(filepath)
  av_pre, rec, acc = classify(clf, X_tr, Y_tr, X_te, Y_te)
  print('accuracy ', acc)
  print('recall ', rec)
  print('precision ', av_pre)

bench()
