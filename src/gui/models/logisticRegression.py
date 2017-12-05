from classifier import Classifier
import sklearn.linear_model as skl_lm

class LogisticRegression(Classifier):
    def __init__(self):
        self.name = "Max Entropy"
        self.classifier = skl_lm.LogisticRegression()

    def fit(self, data_train, train_labels):
        self.classifier.fit(data_train, train_labels)

    def predict(self, data_test):
        return self.predict(data_test)
