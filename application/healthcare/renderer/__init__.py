import os
from matplotlib.pyplot import savefig, clf, figure, plot, close

__author__ = 'mkk'

class Renderer:
    def export(self, data_list, fdir, fname, format='pdf'):
        if not os.path.exists(fdir):
            os.makedirs(fdir)

        cnt = 0
        for data in data_list:
            cnt += 1
            clf()
            figure()
            plot(data)
            savefig(fdir+'/'+fname+'_'+str(cnt)+'.'+format, transparent=True, bbox_inches='tight', pad_inches=0, format=format)
            close()