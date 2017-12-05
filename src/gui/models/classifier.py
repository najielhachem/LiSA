from abc import ABC, abstractmethod

class Classifier(ABC):
    def __init__(self):
        self.name = "Classifier"

    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def predict(self):
        pass
