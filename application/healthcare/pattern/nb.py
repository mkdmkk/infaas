from sklearn.naive_bayes import GaussianNB

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

    def train(self, data, labels):
        """
        Train the decision tree with the training data
        :param data:
        :param labels:
        :return:
        """
        print('Training Data: %s' % (data))
        print('Training Labels: %s' % (labels))
        self.model = GaussianNB()
        self.model = self.model.fit(data, labels)

    def eval(self, obs):
        # print('Testing Result: %s; %s' % (self.model.predict(obs), self.model.predict_proba(obs)))
        print('Testing Result: %s' % self.model.predict(obs))
