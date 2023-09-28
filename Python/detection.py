import random

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import morlet
from matplotlib.animation import FuncAnimation

# Parameters
freq = 1
width = 500
t = np.linspace(-5 * np.pi, 5 * np.pi, width)

# Initialize the figure and axis
fig, ax = plt.subplots(figsize=(10, 6))
line_real, = ax.plot([], [], label='Real part')

# Set plot limits
ax.set_xlim(-5 * np.pi, 5 * np.pi)
ax.set_ylim(-1, 1)
ax.set_title('Morlet Wavelet')
ax.set_xlabel('Time')
ax.set_ylabel('Amplitude')
ax.legend()
ax.grid(True)

def plot_values(arr):
    x_values = [(0 + i*0.1) for i,el in enumerate(arr)]
    y_values = arr

    xmin = min(x_values)
    xmax = max(x_values)
    ax.set_xlim(xmin-0.5, xmax+0.5)


    ymin = min(y_values)
    ymax = max(y_values)
    ax.set_ylim(ymin-0.5, ymax+0.5)

    print(x_values, y_values)
    line_real.set_data(x_values, y_values)
    plt.show()


def make_it_real(arr):
    out = []
    for el in arr:
        out.append(float(el))
    return out

def update(frame):
    global freq
    global direction
    freq += 0.01
    morlet_wavelet = morlet(M=width, w=1, s=1, complete=True)
    morlet_wavelet = make_it_real(morlet_wavelet)
    line_real.set_data(t, np.real(morlet_wavelet))
    return line_real

#ani = FuncAnimation(fig, update, frames=10, interval=2, blit=True)
#plt.show()


plot_values([1,2,3,4,3,2,3,1])