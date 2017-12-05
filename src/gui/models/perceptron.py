from classifier import Classifier
import sklearn.linear_model as skl_lm

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
        return self.predict(data_test)
