import numpy as np 
from pylab import *
from scipy.signal import butter, lfilter

class Peakpicker:

    radius = 0
    rel_thre = 0.0
    abs_thre = 0.0

    def __init__(self):
        return

    def configure(self, radius=0.0, rel_thre=0.0, abs_thre=0.0):
        self.radius = int(radius)
        self.rel_thre = rel_thre
        self.abs_thre = abs_thre

        return
    
    def process(self, arr):

        self.data = 1. * arr

        # find all maxima
        self.max_data = np.zeros(len(self.data))
        for n in np.arange(self.radius, len(self.data)-self.radius):
            idx = np.arange(n-self.radius, n+self.radius)
            if(np.argmax(self.data[idx]) == self.radius):
                self.max_data[n] = self.data[n]
            else:
                self.max_data[n] = 0

        # # find all maxima that are greater than thre_std * std(data)
        # std_data = np.std(self.data)
        # self.thre_dyn = self.rel_thre * std_data
        # self.thre_dyn_arr = self.thre_dyn * np.ones(len(self.data))
        # for n, e in enumerate(self.max_data):
        #     if e < self.thre_dyn:
        #         self.max_data[n] = 0

        for n, e in enumerate(self.max_data):
            if e < self.abs_thre:
                self.max_data[n] = 0

        self.odata = self.max_data
        self.locs = np.arange(0, len(self.odata)) * (self.odata != 0)
        self.locs = self.locs[self.locs > 0]

        return

    pass

def main():

    N = 1000
    K = 21
    arr = np.zeros(N)
    mu = 0.0
    std = 1.0
    b,a = butter(5, 0.05, btype='low', analog=False, output='ba')
    
    for n in arange(1, N):
        arr[n] = arr[n-1] + np.random.normal(mu, std, 1)
    
    arr = lfilter(b, a, arr)

    pp = Peakpicker()
    pp.configure(radius=50, rel_thre=0.1, abs_thre=10.0)
    pp.process(arr)

    figure(); plot(arr, lw=1); plot(pp.locs, arr[pp.locs], 'ro'); show()

    return

if __name__ == '__main__':
    main()
    