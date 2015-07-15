from sklearn import tree
from sklearn.externals.six import StringIO
from sklearn.tree import DecisionTreeClassifier
import pydot

__author__ = 'Moon Kwon Kim <mkdmkk@gmail.com>'

class PatternBasedDiagnosis:
    """
    Pattern Based Diagnosis with Decision Tree
    """

    __slots__ = [
        "model"
    ]

    def __init__(self):
        pass

    def export(self, fpath):
        """
        Export the decision tree as a PDF file
        :return: None
        """
        dot_data = StringIO()
        tree.export_graphviz(self.model, out_file=dot_data)
        graph = pydot.graph_from_dot_data(dot_data.getvalue())
        graph.write_pdf(fpath)

    def train(self, data, labels):
        """
        Train the decision tree with the training data
        :param data:
        :param labels:
        :return:
        """
        print('Training Data: %s' % (data))
        print('Training Labels: %s' % (labels))
        self.model = DecisionTreeClassifier(criterion="entropy") # C4.5 Decision Tree
        self.model = self.model.fit(data, labels)

    def eval(self, obs):
        print('Testing Result: %s; %s' % (self.model.predict(obs), self.model.predict_proba(obs)))
