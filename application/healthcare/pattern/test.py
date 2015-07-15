import math

__author__ = 'mkk'

from application.healthcare.loader.ecg import ptbdb
import numpy as np
import time
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier

def train(self, data, labels):
    """
    Train the decision tree with the training data
    :param data:
    :param labels:
    :return:
    """
    print('Training Data: %s' % (data))
    print('Training Labels: %s' % (labels))
    self.model = KNeighborsClassifier(n_neighbors=3, algorithm='ball_tree')
    self.model = self.model.fit(data, labels)

def eval(self, obs):
    print('Testing Result: %s; %s' % (self.model.predict(obs), self.model.predict_proba(obs)))
    # print('Testing Result: %s' % self.model.predict(obs))

# @profile(precision=4)
def diagnose():
    # ----------
    # Loading Dataset
    #
    size = 600

    # ----------
    # Training
    #

    # Myocardial Infarction
    X = ptbdb.segments_pat1
    X = np.append(X, ptbdb.segments_pat2, axis=0)
    X = np.append(X, ptbdb.segments_pat3, axis=0)
    # Hypertrophy
    X = np.append(X, ptbdb.segments_pat212, axis=0)
    X = np.append(X, ptbdb.segments_pat210, axis=0)
    X = np.append(X, ptbdb.segments_pat159, axis=0)
    # Bundle Branch Block
    X = np.append(X, ptbdb.segments_pat213, axis=0)
    X = np.append(X, ptbdb.segments_pat175, axis=0)
    X = np.append(X, ptbdb.segments_pat171, axis=0)
    # Healthy Control
    X = np.append(X, ptbdb.segments_pat244, axis=0)
    X = np.append(X, ptbdb.segments_pat245, axis=0)
    X = np.append(X, ptbdb.segments_pat246, axis=0)
    X = np.append(X, ptbdb.segments_pat247, axis=0)
    X = np.append(X, ptbdb.segments_pat248, axis=0)

    y = ['Myocardial Infarction']*len(ptbdb.segments_pat1)
    y = np.append(y, ['Myocardial Infarction']*len(ptbdb.segments_pat2))
    y = np.append(y, ['Myocardial Infarction']*len(ptbdb.segments_pat3))
    y = np.append(y, ['Hypertrophy']*len(ptbdb.segments_pat212))
    y = np.append(y, ['Hypertrophy']*len(ptbdb.segments_pat210))
    y = np.append(y, ['Hypertrophy']*len(ptbdb.segments_pat159))
    y = np.append(y, ['Bundle Branch Block']*len(ptbdb.segments_pat213))
    y = np.append(y, ['Bundle Branch Block']*len(ptbdb.segments_pat175))
    y = np.append(y, ['Bundle Branch Block']*len(ptbdb.segments_pat171))
    y = np.append(y, ['Healthy Control']*len(ptbdb.segments_pat244))
    y = np.append(y, ['Healthy Control']*len(ptbdb.segments_pat245))
    y = np.append(y, ['Healthy Control']*len(ptbdb.segments_pat246))
    y = np.append(y, ['Healthy Control']*len(ptbdb.segments_pat247))
    y = np.append(y, ['Healthy Control']*len(ptbdb.segments_pat248))


    fig = plt.figure(facecolor="white")
    for i in range(len(ptbdb.segments_pat1)):
        plt.subplot(math.ceil(len(ptbdb.segments_pat1)/2.0), 2, i+1)
        plt.plot(ptbdb.segments_pat1[i])
        plt.title("Segment %s" % str(i+1))
    fig.subplots_adjust(wspace=0.5, hspace=1)
    fig.suptitle("ECG (Myocardial infarction)")
    plt.show()

    start = time.time()
    print("Start... %s" % start)
    train(X, y)

    # ----------
    # Export the decision tree
    #
    #  pbd.export("../output/pattern/dt.pdf")

    # ----------
    # Evaluation (Inference)
    #

    location = 7

    # MI, MI, MI, H, H, BBB, BBB, HC, HC, HC
    eval(ptbdb.data_pat1[640+730*location-size/2-1:640+730*location+size/2])
    eval(ptbdb.data_pat2[690+720*location-size/2-1:690+720*location+size/2])
    eval(ptbdb.data_pat3[1680+800*location-size/2-1:1680+800*location+size/2])
    eval(ptbdb.data_pat212[710+760*location-size/2-1:710+760*location+size/2])
    eval(ptbdb.data_pat159[1200+700*location-size/2-1:1200+700*location+size/2])
    eval(ptbdb.data_pat171[450+700*location-size/2-1:450+700*location+size/2])
    eval(ptbdb.data_pat175[1250+790*location-size/2-1:1250+790*location+size/2])
    eval(ptbdb.data_pat244[1290+800*location-size/2-1:1290+800*location+size/2])
    eval(ptbdb.data_pat248[1100+920*location-size/2-1:1100+920*location+size/2])
    eval(ptbdb.data_pat245[780+760*location-size/2-1:780+760*location+size/2])

    end = time.time()
    print("Ended. %s" % end)
    print("Elapsed Time: %s" % int(round((end-start)*1000)))

    # ----------
    # Export pdf files showing the training data and the testing data
    #
    # renderer = Renderer()
    # renderer.export(segments_pat1, settings.BASE_DIR+'/output/pattern/training_dataset/pat1', 'pat1')
    # renderer.export(segments_pat1, settings.BASE_DIR+'/output/pattern/training_dataset/pat2', 'pat2')
    # renderer.export(segments_pat3, settings.BASE_DIR+'/output/pattern/training_dataset/pat3', 'pat3')
    # renderer.export([data_pat1[680+740*10-size/2-1:680+740*10+size/2]], settings.BASE_DIR+'/output/pattern/testing_dataset', 'pat1')
    # renderer.export([data_pat2[700+740*10-size/2-1:700+740*10+size/2]], settings.BASE_DIR+'/output/pattern/testing_dataset', 'pat2')
    # renderer.export([data_pat3[700+740*10-size/2-1:700+740*10+size/2]], settings.BASE_DIR+'/output/pattern/testing_dataset', 'pat3')

if __name__ == "__main__":
    diagnose()
