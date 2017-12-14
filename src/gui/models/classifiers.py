from abc import ABC, abstractmethod

import sklearn.svm as skl_svm
import sklearn.linear_model as skl_lm
import sklearn.naive_bayes as skl_nb

import pickle

# Abstract Class: Classifier

class Classifier(ABC):

    """ This is an abstract class. It is used as an interface between all our
        classifiers and our controllers.

        Different implementations of our classifiers inherite from this class.
        You must implement both fit and predict functions.
    """

    def __init__(self):
        self.name = "Classifier"
        self.classifier = Null

    @abstractmethod
    def fit(self, data_train, train_labels):
        pass

    @abstractmethod
    def predict(self, data_test):
        pass

    def save(self, path="data/trained_classifiers/"):
        with open(path + self.name, "wb") as file:
            file.write(pickle.dumps(self.classifier))

    def load(self, path="data/trained_classifiers/"):
        try:
            with open(path + self.name, "rb") as file:
                self.classifier = pickle.loads(b''.join(file.readlines()))
        except:
            print("This classifier has never been saved before")


# Naive Bayes Classifiers

class BernoulliNB(Classifier):
    def __init__(self, alpha=1.0):
        """ BernoulliNB classifier imported from  sklearn
        Args:
            alpha (float, optional (default=1.0)): Additive (Laplace/Lidstone)
                smoothing parameter (0 for no smoothing).
        """

        self.name = "Bernoulli NB"
        self.classifier = skl_nb.BernoulliNB(alpha)

    def fit(self, data_train, train_labels):
        self.classifier.fit(data_train, train_labels)

    def predict(self, data_test):
        return self.classifier.predict(data_test)

class MultinomialNB(Classifier):
    def __init__(self, alpha=1.0):
        """ MultinomialNB classifier imported from  sklearn
        Args:
            alpha (float, optional (default=1.0)): Additive (Laplace/Lidstone)
                smoothing parameter (0 for no smoothing).
        """

        self.name = "Multinomial NB"
        self.classifier = skl_nb.MultinomialNB(alpha)

    def fit(self, data_train, train_labels):
        self.classifier.fit(data_train, train_labels)

    def predict(self, data_test):
        return self.classifier.predict(data_test)


# Linear Models Classifier

class Perceptron(Classifier):
    def __init__(self, max_iter):
        """ Perceptron classifier imported from  sklearn
        Args:
            max_iter (int, optional): The maximum number of passes over the
                training data (aka epochs). It only impacts the behavior in the
                fit method, and not the partial_fit. Defaults to 5. Defaults
                to 1000 from 0.21, or if tol is not None.
        """

        self.name = "Perceptron"
        self.classifier = skl_lm.RidgeClassifier(max_iter=max_iter)

    def fit(self, data_train, train_labels):
        self.classifier.fit(data_train, train_labels)

    def predict(self, data_test):
        return self.classifier.predict(data_test)


class LogisticRegression(Classifier):
    def __init__(self):
        self.name = "Max Entropy"
        self.classifier = skl_lm.LogisticRegression()

    def fit(self, data_train, train_labels):
        self.classifier.fit(data_train, train_labels)

    def predict(self, data_test):
        return self.classifier.predict(data_test)

class Ridge(Classifier):
    def __init__(self, tol, solver):
        """ Ridge classifier imported from  sklearn
        Args:
            tol (float): Precision of the solution.
            solver ({‘auto’, ‘svd’, ‘cholesky’, ‘lsqr’, ‘sparse_cg’, ‘sag’, ‘saga’}):
                Solver to use in the computational routines (see sklearn documentation)
        """

        self.name = "Bernoulli NB"
        self.classifier = skl_lm.RidgeClassifier(tol=tol, solver=solver)

    def fit(self, data_train, train_labels):
        self.classifier.fit(data_train, train_labels)

    def predict(self, data_test):
        return self.classifier.predict(data_test)

# SVM Classifiers

class LinearSVC(Classifier):
    def __init__(self, random_state = None):
        """ LinearSVC classifier imported from  sklearn
        Args:
            random_state (float): The seed of the pseudo random number generator
                to use when shuffling the data (see sklearn documentation)
        """

        self.name = "SVM"
        self.classifier = skl_svm.LinearSVC(random_state=random_state)

    def fit(self, data_train, train_labels):
        self.classifier.fit(data_train, train_labels)

    def predict(self, data_test):
        return self.classifier.predict(data_test)
def get_classifiers():
    clf1 = LinearSVC()
    clf2 = Ridge()
    clf3 = MultinomialNB()
    clfs = [clf1, clf2, clf3]
    dic_clfs = {}
    for clf in clfs:
        dic_clfs[clf.name] = clf
    return dic_clfs
