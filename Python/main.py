import random
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import csv
from tkinter.filedialog import askopenfilename
from RangeSlider.RangeSlider import RangeSliderH

global file
global valuesDict

def CSVToDict(file):
    out = dict()
    with open(file) as csvfile:
        rdr = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in rdr:
            rowToAdd = []
            for val in row[1:]:
                rowToAdd.append(int(val.strip()))
            out[float(row[0].strip())] = rowToAdd
    return out

def main():
    root = tk.Tk()
    root.title("ManoMap Remake")

    #todo
    #load data
    def openFile():
        global file
        global valuesDict
        file = askopenfilename()
        valuesDict = CSVToDict(file)
    button = tk.Button(root, text="Select Input File", command=openFile)
    button.pack(side=tk.LEFT, pady=10, padx=10)
    #normal/filtered vs median filtering vragen
    #tijd filter eventueel
    #color values
    #detect events
    #tijdstippen toevoegen
    #darmsecties indelen



    var = tk.StringVar()
    label = tk.Label(root, textvariable=var)
    var.set("Visible sensors:")
    label.pack()
    hVar1 = tk.DoubleVar(value=0)
    hVar2 = tk.DoubleVar(value=40)
    sensorSlider = RangeSliderH(root, [hVar1, hVar2], Width=400, Height=65, padX=17, min_val=0, max_val=40, show_value=True, step_size=1, bar_radius=5, digit_precision='.0f')
    sensorSlider.pack()


    def showPlotPressed():
        slidervals = sensorSlider.getValues()
        first_sensor = int(slidervals[0])
        last_sensor = int(slidervals[1])
        showPlot(first_sensor, last_sensor)

    button = tk.Button(root, text="Plot Data", command=showPlotPressed)
    button.pack(side=tk.LEFT, pady=10, padx=10)
    button = tk.Button(root, text="Detect Events")
    button.pack(side=tk.LEFT,pady=10, padx=10)

    root.mainloop()


def showPlot(firstSensor, lastSensor):
    global valuesDict
    p = dictionary_to_ndarray(valuesDict)
    plt.imshow(p, cmap='gnuplot2', interpolation='nearest', aspect='auto', vmin= 0, vmax=100)
    plt.yticks(np.arange(firstSensor, lastSensor + 1, 2))

    plt.axis([0, int(list(valuesDict)[-1]), lastSensor, firstSensor])
    plt.show()

#https://stackoverflow.com/questions/20398920/physically-stretch-plot-in-horizontal-direction-in-python
#voor testing purposes
def genPerlinNoise():
    def perlin(x, y, seed=0):
        np.random.seed(seed)
        p = np.arange(256, dtype=int)
        np.random.shuffle(p)
        p = np.stack([p, p]).flatten()
        xi, yi = x.astype(int), y.astype(int)
        xf, yf = x - xi, y - yi
        u, v = fade(xf), fade(yf)
        n00 = gradient(p[p[xi] + yi], xf, yf)
        n01 = gradient(p[p[xi] + yi + 1], xf, yf - 1)
        n11 = gradient(p[p[xi + 1] + yi + 1], xf - 1, yf - 1)
        n10 = gradient(p[p[xi + 1] + yi], xf - 1, yf)
        x1 = lerp(n00, n10, u)
        x2 = lerp(n01, n11, u)
        return lerp(x1, x2, v)


    def lerp(a, b, x):
        return a + x * (b - a)


    def fade(t):
        return 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3


    def gradient(h, x, y):
        vectors = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
        g = vectors[h % 4]
        return g[:, :, 0] * x + g[:, :, 1] * y

    p = np.zeros((41, 1000))
    for i in range(4):
        freq = 2 ** i
        liny = np.linspace(0, freq, 1000, endpoint=False)
        linx = np.linspace(0, freq, 41, endpoint=False)
        x, y = np.meshgrid(liny, linx)
        p = perlin(x, y, seed=random.randint(0,200000)) / freq + p
    return p

def dictionary_to_ndarray(data_dict):
    values = list(data_dict.values())
    nd_array = np.stack(values)
    return nd_array.transpose()

if __name__ == '__main__':
    main()

