from classifier import Classifier
import sklearn.linear_model as skl_lm

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
        return self.predict(data_test)
