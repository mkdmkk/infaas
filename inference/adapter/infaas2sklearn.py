from sklearn.tree import DecisionTreeClassifier

__author__ = 'mkk'

class DecisionTree():
    def __init__(self):
        self.sklearn_decisiontree = DecisionTreeClassifier()

    def train(self, data):
        self.sklearn_decisiontree.fit()

    def infer(self, data):
        self.sklearn_decisiontree.predict()