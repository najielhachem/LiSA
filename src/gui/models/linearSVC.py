from classifier import Classifier
import sklearn.svm as skl_svm

class LinearSVC(Classifier):
    def __init__(self, random_state):
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
        return self.predict(data_test)
