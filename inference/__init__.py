import numpy
from sklearn.naive_bayes import GaussianNB

__author__ = 'mkk'

if __name__ == "__main__":
    nb = GaussianNB()
    ctx1 = numpy.array([1,2,3,4,5,6,7,8,9,100])
    ctx2 = numpy.array([1,2,3,4,5,16,7,18,9,100])
    obs = numpy.array([0.1,5,5,5,5,15,5,15,5,115])

    nb.fit(numpy.array([ctx1, ctx2]), [1,2])
    print(nb.predict_log_proba(obs))