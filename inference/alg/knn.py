__author__ = 'mkk'

from numpy import *
import operator
import numpy as np
import matplotlib.pyplot as plt

def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()
    classCount={}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def tutorial():
    x_c1 = np.array([[1,1],[1,3],[2,4],[3,2],[3,1],[4,2],[4,8],[5,4],[6,9],[6,1]])
    x_c2 = np.array([[6,7],[7,7],[7,3],[8,3],[8,5],[9,7],[9,4],[8,9],[9,1],[7,5]])
    y_c1 = np.array([1]*len(x_c1))
    y_c2 = np.array([2]*len(x_c2))
    print(x_c1)
    print(x_c1[:,0])
    print(x_c1[:,1])
    fig = plt.figure(facecolor="w")
    plt.plot(x_c1[:,0],x_c1[:,1], 'bo')
    plt.plot(x_c2[:,0],x_c2[:,1], 'ro')
    plt.xlim([0,10])
    plt.ylim([0,10])
    plt.show()

# for tutorial
tutorial()
