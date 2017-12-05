from classifier import Classifier
import sklearn.linear_model as skl_lm

class Perceptron(Classifier):
    def __init__(self, max_iter):
        self.name = "Perceptron"
        self.classifier = skl_lm.RidgeClassifier(max_iter=max_iter)

    def fit(self, data_train, train_labels):
        self.classifier.fit(data_train, train_labels)

    def predict(self, data_test):
        return self.predict(data_test)
