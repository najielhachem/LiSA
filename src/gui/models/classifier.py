from abc import ABC, abstractmethod

class Classifier(ABC):

    """ This is an abstract class. It is used as an interface between all our
        classifiers and our controllers.

        Different implementations of our classifiers inherite from this class.
        You must implement both fit and predict functions.
    """

    def __init__(self):
        self.name = "Classifier"

    @abstractmethod
    def fit(self, data_train, train_labels):
        pass

    @abstractmethod
    def predict(self, data_test):
        pass
