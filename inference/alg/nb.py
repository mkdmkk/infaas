__author__ = 'mkk'

import numpy as np

def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    #1 is abusive, 0 not
    return postingList,classVec

def createVocabList(dataSet):
    vocabSet = set([])  #create empty set
    for document in dataSet:
        vocabSet = vocabSet | set(document) #union of the two sets
    return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else: print "the word: %s is not in my Vocabulary!" % word
    return returnVec

def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)
    print("Len. of Training Data: %s" % numTrainDocs)
    numWords = len(trainMatrix[0])
    print("Len. of Training Data [0]: %s" % numWords)
    pAbusive = sum(trainCategory)/float(numTrainDocs) # p(c=1), p(c=0) = 1-p(c=1)
    p0Num = np.ones(numWords); p1Num = np.ones(numWords)      #change to ones()
    print("p0Num %s p1Num %s" % (p0Num, p1Num))
    p0Denom = 2.0; p1Denom = 2.0                        #change to 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
        print("p0Num %s p1Num %s" % (p0Num, p1Num))
        print("p0Denom %s p1Denom %s" % (p0Denom, p1Denom))
    p1Vect = np.log(p1Num/p1Denom)          #change to log()
    p0Vect = np.log(p0Num/p0Denom)          #change to log()
    return p0Vect,p1Vect,pAbusive

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + np.log(pClass1)    #element-wise mult
    p0 = sum(vec2Classify * p0Vec) + np.log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0

def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec

print("----- Preparing Data")
postingList, classVec = loadDataSet()
vocabList = createVocabList(postingList)
print("Data: %s" % postingList)
print("Label: %s" % classVec)
print("Vocab List: %s" % vocabList)
trainMat=[]
for postinDoc in postingList:
    trainMat.append(setOfWords2Vec(vocabList, postinDoc))
print("Matrix: %s" % trainMat)

print("----- Learning")
p0V,p1V,pAb = trainNB0(trainMat,classVec)
print("p(x_i|c=0) = %s" % p0V)
print("p(x_i|c=1) = %s" % p1V)
print("p(c=1) = %s" % pAb)

