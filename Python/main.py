import random
import tkinter as tk
import matplotlib.pyplot
import matplotlib.pyplot as plt
import numpy as np
import csv
from tkinter.filedialog import askopenfilename
from RangeSlider.RangeSlider import RangeSliderH

global file
global valuesDict

differentialMode = False

#Functie die CSV (of txt mits juiste syntax) file path input neemt en een dictionary returnt. Timestamps zijn keys.
def CSVToDict(file):
    out = dict()
    with open(file) as csvfile:
        rdr = csv.reader(csvfile, delimiter=' ', quotechar='|')
        rownumber = 1
        for row in rdr:
            rownumber+=1
            if rownumber < 10:
                continue
            rowToAdd = []
            for val in row[1:]:
                currentVal = int(val.strip())
                rowToAdd.append(currentVal)
            out[rownumber] = rowToAdd
    return out

#UI
def main():
    root = tk.Tk()
    root.title("ManoMap Remake")
    fileTitle = tk.StringVar()
    def openFile():
        global file
        global valuesDict
        fileTitle.set("Loading file...")
        file = askopenfilename()
        valuesDict = CSVToDict(file)
        fileTitle.set(file.title())
    button = tk.Button(root, text="Select Input File", command=openFile)
    button.pack(side=tk.LEFT, pady=10, padx=10)

    fileLabel = tk.Label(root, textvariable=fileTitle)
    fileTitle.set("No file selected")
    fileLabel.pack()
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

    thresholdText = tk.StringVar()
    label = tk.Label(root, textvariable=thresholdText)
    thresholdText.set("Thresholds:")
    label.pack()
    hVar3 = tk.DoubleVar(value=10)
    hVar4 = tk.DoubleVar(value=200)
    thresholdSlider = RangeSliderH(root, [hVar3, hVar4], Width=400, Height=65, padX=17, min_val=0, max_val=500, show_value=True, step_size=1, bar_radius=5, digit_precision='.0f')
    thresholdSlider.pack()

    def showPlotPressed():
        slidervals = sensorSlider.getValues()
        first_sensor = int(slidervals[0])
        last_sensor = int(slidervals[1])
        thresholdVals = thresholdSlider.getValues()
        minThreshold = int(thresholdVals[0])
        maxThreshold = int(thresholdVals[1])
        showPlot(first_sensor, last_sensor, minThreshold, maxThreshold)

    button = tk.Button(root, text="Plot Data", command=showPlotPressed)
    button.pack(side=tk.LEFT, pady=10, padx=10)
    button = tk.Button(root, text="Detect Events")
    button.pack(side=tk.LEFT,pady=10, padx=10)

    root.mainloop()

#Toont plot in matplotlib nieuwe window. Kan naar externe module gerefactord worden
def showPlot(firstSensor, lastSensor, minThreshold, maxThreshold):
    global valuesDict
    matplotlib.pyplot.close('all')
    p = dictionary_to_ndarray(valuesDict)

    minT = minThreshold
    maxT = maxThreshold
    cmap = 'inferno'
    #te veel performance loss
    #p = smooth_ndArray(p, 5)

    #als differentialMode aan staat, toon het verschil ten opzichte van vorige waarde ipv de waarde zelf.
    if differentialMode:
        minT = -3
        maxT = 3
        cmap = 'coolwarm'
        p = calculate_differences(p)
    tmp = plt.imshow(p, cmap=cmap, interpolation='none', aspect='auto', vmin=minT, vmax=maxT)
    plt.yticks(np.arange(firstSensor, lastSensor + 1, 2))
    plt.axis([0, len(list(valuesDict)), lastSensor, firstSensor])
    cb = plt.colorbar(tmp)
    plt.show()


#zet een dictionary om naar een 2D Numpy Array (gebruikt om te plotten, row 1 = sensor 1 etc...)
def dictionary_to_ndarray(data_dict):
    values = list(data_dict.values())
    nd_array = np.stack(values)
    return nd_array.transpose()

def calculate_differences(arr):
    num_rows, num_cols = len(arr), len(arr[0])
    result = []
    for row in arr:
        new_row = [row[0]]
        for i in range(1, num_cols):
            difference = row[i] - row[i - 1]
            new_row.append(difference)
        result.append(new_row)
    return result

def average(arr):
    out = 0
    for i in arr:
        out += i
    return out/len(arr)

def smooth_row(arr, filter_length):
    out = []
    for i in range(len(arr)-1):
        lowerBound = max(0, i-filter_length)
        upperBound = min(len(arr)-1, i+filter_length)
        out.append(average(arr[lowerBound:upperBound]))
    return out

def smooth_ndArray(ndarr, filterLength):
    out = []
    for row in ndarr:
        out.append(smooth_row(row, filterLength))
    return np.array(out)

if __name__ == '__main__':
    main()

