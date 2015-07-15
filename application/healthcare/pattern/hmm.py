from matplotlib.pyplot import plot, show, figure
from hmmlearn.hmm import GaussianHMM
import numpy as np
import time
from utils.csv_loader import CSVLoader
from application.healthcare.loader.ecg import ptbdb

__author__ = 'mkk'

class HMM:
    __slots__ = [
        "model"
    ]

    def __init__(self):
        pass


    def draw(self, data):
        figure()
        plot(range(len(data)),data,alpha=0.8,color='red')
        show()


    def train(self, data, n_components):
        print("Training Data: %s" % data)
        self.data = data
        self.model = GaussianHMM(n_components, algorithm='viterbi', covariance_type='diag')
        X = np.reshape(data, (len(data),1))
        self.model = self.model.fit([X])

        self.hidden_states = self.model.predict(X)
        print("Sequence of States: " % self.hidden_states)


    def eval(self, obs):
        print("Testing Data: %s" % obs)
        X = np.reshape(obs, (len(obs),1))
        print("Eval: %s" % str(self.model.score(X)))


    def plot(self):
        fig = figure(facecolor="white")
        ax = fig.add_subplot(111)

        for i in range(self.model.n_components):
            # use fancy indexing to plot data in each state
            idx = (self.hidden_states == i)
            ax.plot(np.array(range(len(self.data)))[idx], np.array(self.data)[idx], '.', label="State %d" % (i+1))

        ax.legend()
        show()


if __name__ == "__main__":

    # Myocardial Infarction: 1, 2, 3
    # Hypertrophy: 212, 210, 159
    # Bundle Branch Block: 213, 175, 171
    # Healthy Control: 244, 245, 246, 247, 248
    hmm_mi = HMM()
    hmm_h = HMM()
    hmm_bbb = HMM()
    hmm_hc = HMM()

    start = time.time()
    print("Start... %s" % start)

    hmm_mi.train(np.append(
        ptbdb.data_pat1,
        [ptbdb.data_pat2,
        ptbdb.data_pat3]), 4)
    hmm_h.train(np.append(
        ptbdb.data_pat212,
        [ptbdb.data_pat210,
        ptbdb.data_pat159]), 4)
    hmm_bbb.train(np.append(
        ptbdb.data_pat213,
        [ptbdb.data_pat175,
        ptbdb.data_pat171]), 4)
    hmm_hc.train(np.append(
        ptbdb.data_pat244,
        [ptbdb.data_pat245,
        ptbdb.data_pat246,
        ptbdb.data_pat247,
        ptbdb.data_pat248]), 4)

    size = 600
    location = 7
    # MI, MI, MI, H, H, BBB, BBB, HC, HC, HC
    hmm_mi.eval(ptbdb.data_pat1[640+730*location-size/2-1:640+730*location+size/2])
    hmm_mi.eval(ptbdb.data_pat2[690+720*location-size/2-1:690+720*location+size/2])
    hmm_mi.eval(ptbdb.data_pat3[1680+800*location-size/2-1:1680+800*location+size/2])
    hmm_mi.eval(ptbdb.data_pat212[710+760*location-size/2-1:710+760*location+size/2])
    hmm_mi.eval(ptbdb.data_pat159[1200+700*location-size/2-1:1200+700*location+size/2])
    hmm_mi.eval(ptbdb.data_pat171[450+700*location-size/2-1:450+700*location+size/2])
    hmm_mi.eval(ptbdb.data_pat175[1250+790*location-size/2-1:1250+790*location+size/2])
    hmm_mi.eval(ptbdb.data_pat244[1290+800*location-size/2-1:1290+800*location+size/2])
    hmm_mi.eval(ptbdb.data_pat248[1100+920*location-size/2-1:1100+920*location+size/2])
    hmm_mi.eval(ptbdb.data_pat245[780+760*location-size/2-1:780+760*location+size/2])

    end = time.time()
    print("Ended. %s" % end)
    print("Elapsed Time: %s" % int(round((end-start)*1000)))
