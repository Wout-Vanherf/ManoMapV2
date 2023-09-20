import random
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import csv
from tkinter.filedialog import askopenfilename
from RangeSlider.RangeSlider import RangeSliderH

global file
global valuesDict

#Functie die CSV (of txt mits juiste syntax) file path input neemt en een dictionary returnt. Timestamps zijn keys.
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
        print(type(file))
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

#Toont plot in matplotlib nieuwe window. Kan naar externe module gerefactord worden
def showPlot(firstSensor, lastSensor):
    global valuesDict
    p = dictionary_to_ndarray(valuesDict)
    plt.imshow(p, cmap='inferno', interpolation='nearest', aspect='auto', vmin= 10, vmax=100)
    plt.yticks(np.arange(firstSensor, lastSensor + 1, 2))

    plt.axis([0, int(list(valuesDict)[-1]), lastSensor, firstSensor])
    plt.show()

#zet een dictionary om naar een 2D Numpy Array (gebruikt om te plotten, row 1 = sensor 1 etc...)
def dictionary_to_ndarray(data_dict):
    values = list(data_dict.values())
    nd_array = np.stack(values)
    return nd_array.transpose()

if __name__ == '__main__':
    main()

