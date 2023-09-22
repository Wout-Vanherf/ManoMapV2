import tkinter as tk
import signalplot
import heatplot
import manoutils
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from RangeSlider.RangeSlider import RangeSliderH

global file
global valuesDict

differentialMode = False

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
        valuesDict = manoutils.CSVToDict(file)
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
    thresholdSlider = RangeSliderH(root, [hVar3, hVar4], Width=400, Height=65, padX=17, min_val=0, max_val=500, show_value=True, step_size=5, bar_radius=5, digit_precision='.0f')
    thresholdSlider.pack()

    def showPlotPressed():
        slidervals = sensorSlider.getValues()
        first_sensor = int(slidervals[0])
        last_sensor = int(slidervals[1])
        thresholdVals = thresholdSlider.getValues()
        minThreshold = int(thresholdVals[0])
        maxThreshold = int(thresholdVals[1])
        heatplot.showPlot(first_sensor, last_sensor, minThreshold, maxThreshold, differentialMode, valuesDict, colormap='Greys')

    def showSignalsPressed():
        slidervals = sensorSlider.getValues()
        first_sensor = int(slidervals[0])
        last_sensor = int(slidervals[1])
        thresholdVals = thresholdSlider.getValues()
        minThreshold = int(thresholdVals[0])
        maxThreshold = int(thresholdVals[1])
        signalplot.show_combined_plot(valuesDict)
    
    def detectEventsPressed():
        distance = inputtxt.get("1.0", "end-1c")
        try:
            distance = int(distance)
            print(distance)
        except:
            messagebox.showinfo("Error", "You can only input a number in the distance field.")


    distanceText = tk.StringVar()
    label = tk.Label(root, textvariable=distanceText)
    distanceText.set("distance between sensors:")
    label.pack()
    inputtxt = tk.Text(root,
                   height = 1,
                   width = 10)
    inputtxt.pack()
    
    button = tk.Button(root, text="Plot Data", command=showPlotPressed)
    button.pack(side=tk.LEFT, pady=10, padx=10)

    signalButton = tk.Button(root, text="Plot signals", command=showSignalsPressed)
    signalButton.pack(side=tk.LEFT, pady=10, padx=10)


    button = tk.Button(root, text="Detect Events", command=detectEventsPressed)
    button.pack(side=tk.LEFT,pady=10, padx=10)

    root.mainloop()

if __name__ == '__main__':
    main()

