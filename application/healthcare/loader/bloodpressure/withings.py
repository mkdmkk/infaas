from INFaaS import settings

__author__ = 'mkk'

from numpy import genfromtxt

DATASET_ROOT = settings.BASE_DIR+"/media/healthcare/dataset/bloodpressure"

# Load dataset
data_bp001 = genfromtxt(DATASET_ROOT+"/withings001.csv", delimiter=',')