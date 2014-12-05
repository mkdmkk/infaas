from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

__author__ = 'mkk'

class DecisionTree():
    dt = DT()
    X = [[0,0],[1,1]]
    Y = [0,1]
    dt.fit(X,Y)
    print(dt.predict([[2., 2.]]))

    iris = load_iris()
    print(iris)
    dt.fit(iris.data, iris.target)
