import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import peakpicker as pp
import numpy as np 
from scipy.signal import butter, lfilter

def generate_data():
    N = 1000
    K = 21
    arr = np.zeros(N)
    mu = 0.0
    std = 1.0
    b,a = butter(5, 0.05, btype='low', analog=False, output='ba')
    
    for n in np.arange(1, N):
        arr[n] = arr[n-1] + np.random.normal(mu, std, 1)
    
    arr = lfilter(b, a, arr)
    return arr / np.max(np.absolute(arr))

# -- init
arr = generate_data()
peak = pp.Peakpicker()
peak.configure(radius=50, rel_thre=0.1, abs_thre=0.0)
peak.process(arr)

# -- plot
fig, ax = plt.subplots(figsize=(6,8))
p1 = plt.subplot(211)
plt.title("Random signal")
l1, = plt.plot(arr, lw=1)
l2, = plt.plot(np.ones(len(arr)) * peak.abs_thre, 'g--', label="absolute threshold")
l3, = plt.plot(peak.locs, arr[peak.locs], 'ro', label="peaks")
plt.ylabel("Amplitude")
plt.xlabel("Time (samples)")
plt.grid(linestyle='--', color='gray')
plt.legend()
ax.axis('tight')
plt.ylim([-1.0, +1.0])
fig.tight_layout()

# -- commands
axcolor = 'white'
ax_thre = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor=axcolor)
ax_radius = plt.axes([0.2, 0.10, 0.65, 0.03], facecolor=axcolor)
ax_gen = plt.axes([0.2, 0.15, 0.65, 0.03], facecolor=axcolor)

s_thre = Slider(ax_thre, 'Threshold', -1.0, +1.0, valinit=0.0, valstep=0.1)
s_radius = Slider(ax_radius, 'Radius', 1.0, 100.0, valinit=25.0, valstep=1)
b_gen = Button(ax_gen, 'Generate data', color=axcolor, hovercolor='0.8')

def update_config(val):

    peak.configure(radius=int(s_radius.val), rel_thre=0.1, abs_thre=s_thre.val)
    peak.process(arr)

    l2.set_ydata(np.ones(len(arr)) * peak.abs_thre)
    l3.set_data(peak.locs, arr[peak.locs])

    fig.canvas.draw_idle()

def update_data(val):
    global arr
    arr = generate_data()
    l1.set_ydata(arr)
    return update_config(0)

# -- tie widgets to actions
s_thre.on_changed(update_config)
s_radius.on_changed(update_config)
b_gen.on_clicked(update_data)

plt.show()