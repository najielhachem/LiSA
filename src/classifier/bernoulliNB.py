from classifier import Classifier
import sklearn.naive_bayes as skl_nb

class BernoulliNB(Classifier):
    def __init__(self, alpha):
        self.name = "Bernoulli NB"
        self.classifier = skl_nb.BernoulliNB(alpha)

    def fit(self, data_train, train_labels):
        self.classifier.fit(data_train, train_labels)

    def predict(self, data_test):
        return self.predict(data_test)
