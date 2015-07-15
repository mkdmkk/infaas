__author__ = 'mkk'

import numpy as np

class LogisticRegression:

    def __init__(self, x, y, lam=0.1, alpha=0.3, iter_max=5000):
        self.x = np.array(x) # training dataset
        self.y = np.array(y) # labels for each instance
        x_dim = np.shape(self.x)
        self.m = x_dim[0] # the number of instances
        self.n = x_dim[1] # the number of features
        self.theta = np.ones(self.n+1) # model parameters
        self.lam = lam # regularization parameter
        self.alpha = alpha # step for gradient descent
        self.iter_max = iter_max
        self.x_ = np.concatenate((np.ones((self.m,1)), self.x), axis=1) # bias added training dataset

    def fit(self):
        """
        gradient descent
        :return:
        """
        for i in range(self.iter_max):
            self.theta -= self.alpha * self.grad()

    def hyp(self):
        """
        Sigmoid (logistic) function
        :return:
        """
        return 1. / (1. + np.exp(-self.x_.dot(self.theta)))

    def cost(self):
        """
        Regularized log cost function
        :return:
        """
        # Calculate cost
        h = self.hyp()
        cost = -(1./self.m) * ((self.y.T.dot(np.log(h)) + np.transpose(1-self.y).dot(np.log(1-h))))
        # Regularize
        reg = self.lam/(2.*self.m) * np.power(self.theta, 2)
        cost += reg.sum()
        return cost

    def grad(self):
        grad = (1./self.m) * (np.reshape(self.hyp()-self.y, (self.m,1))) * self.x_
        return np.sum(grad, axis=0)

    def classify(self):
        pass

if __name__ == "__main__":
    from sklearn.datasets import fetch_mldata
    iris = fetch_mldata('iris')
    lr = LogisticRegression(iris.data[iris.target == 1], iris.target[iris.target == 1])

    print(lr.hyp())
    lr.fit()
    print(lr.hyp())