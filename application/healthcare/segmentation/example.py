from matplotlib.pylab import gca, figure, plot, subplot, title, xlabel, ylabel, xlim,show
from matplotlib.lines import Line2D
import segment
import fit
from application.healthcare.loader.ecg import ptbdb

def draw_plot(data,plot_title):
    plot(range(len(data)),data,alpha=0.8,color='red')
    title(plot_title)
    xlabel("Samples")
    ylabel("Signal")
    xlim((0,len(data)-1))

def draw_segments(segments):
    ax = gca()
    for segment in segments:
        line = Line2D((segment[0],segment[2]),(segment[1],segment[3]))
        ax.add_line(line)

# with open("example_data/16265-normalecg.txt") as f:
#     file_lines = f.readlines()

# data = [float(x.split("\t")[2].strip()) for x in file_lines[100:320]]

data = ptbdb.data_pat1[:2000]

# from sklearn.decomposition import PCA
# print(data)
# pca = PCA(n_components=4)
# figure()
# plot(pca.explained_variance_ratio_)
# print(pca.explained_variance_ratio_)
max_error = 0.1

# sliding window with regression
fig = figure(facecolor="w")
fig.add_subplot(2,3,1)
segments = segment.slidingwindowsegment(data, fit.regression, fit.sumsquared_error, max_error)
draw_plot(data,"Sliding window with regression")
draw_segments(segments)

# bottom-up with regression
fig.add_subplot(2,3,2)
segments = segment.bottomupsegment(data, fit.regression, fit.sumsquared_error, max_error)
draw_plot(data,"Bottom-up with regression")
draw_segments(segments)

# top-down with regression
fig.add_subplot(2,3,3)
segments = segment.topdownsegment(data, fit.regression, fit.sumsquared_error, max_error)
draw_plot(data,"Top-down with regression")
draw_segments(segments)

# sliding window with simple interpolation
fig.add_subplot(2,3,4)
segments = segment.slidingwindowsegment(data, fit.interpolate, fit.sumsquared_error, max_error)
draw_plot(data,"Sliding window with simple interpolation")
draw_segments(segments)

# bottom-up with  simple interpolation
fig.add_subplot(2,3,5)
segments = segment.bottomupsegment(data, fit.interpolate, fit.sumsquared_error, max_error)
draw_plot(data,"Bottom-up with simple interpolation")
draw_segments(segments)

# top-down with  simple interpolation
fig.add_subplot(2,3,6)
segments = segment.topdownsegment(data, fit.interpolate, fit.sumsquared_error, max_error)
draw_plot(data,"Top-down with simple interpolation")
draw_segments(segments)

fig.subplots_adjust(wspace=1, hspace=1)
show()

