__author__ = 'mkk'

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn import preprocessing
import application.healthcare.loader.bloodpressure.withings as loader

# Preprocessing; Normalization
X = loader.data_bp001
X = preprocessing.scale(X)

# Prepare model
model = AgglomerativeClustering(n_clusters=5, linkage="average", affinity="euclidean")

# Fit
model.fit(X)

# Plot
label = model.labels_
fig = plt.figure()
ax = p3.Axes3D(fig)
ax.view_init(7, -80)
for l in np.unique(label):
    args = [X[label == l, i] for i in range(np.shape(X)[1])]
    args.append('o')
    ax.plot3D(*tuple(args), color=plt.cm.jet(np.float(l) / np.max(label + 1)))
ax.set_xlabel('time')
ax.set_ylabel('Systolic (mmHg)')
ax.set_zlabel('Diastolic (mmHg)')
plt.show()