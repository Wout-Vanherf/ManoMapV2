import tkinter as tk
import threading
import time
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from RangeSlider.RangeSlider import RangeSliderH

import heatplot
import manoutils
import signalplot

global file
global valuesDict
global commentsDict
commentsDict = dict()

differentialMode = False

#UI 🐀

def main():
    #normal/filtered vs median filtering vragen
    #tijd filter eventueel
    #color values
    #detect events
    #tijdstippen toevoegen
    #darmsecties indelen
    # functions and methods
    def openFile():
        global file
        global valuesDict
        global commentsDict
        commentsDict = dict()
        fileTitle.set("Loading file...")
        file = askopenfilename()
        valuesDict = manoutils.CSVToDict(file)
        fileTitle.set(file.title())

    # Buttons for plotting and detecting
    def showPlotPressed():
        global commentsDict
        slidervals = visibleSensorSlider.getValues()
        first_sensor = int(slidervals[0])
        last_sensor = int(slidervals[1])
        thresholdVals = thresholdSlider.getValues()
        minThreshold = int(thresholdVals[0])
        maxThreshold = int(thresholdVals[1])
        colormap = clicked.get()
        heatplot.showPlot(first_sensor, last_sensor, minThreshold, maxThreshold, differentialMode, valuesDict, commentsDict, colormap=colormap)

    def showSignalsPressed():
        slidervals = visibleSensorSlider.getValues()
        first_sensor = int(slidervals[0])
        last_sensor = int(slidervals[1])
        thresholdVals = thresholdSlider.getValues()
        minThreshold = int(thresholdVals[0])
        maxThreshold = int(thresholdVals[1])
        colormap = clicked.get()
        signalplot.show_combined_plot(valuesDict, first_sensor, last_sensor, minThreshold, maxThreshold, colormap=colormap, opacity=0.7)

    def detectEventsPressed():
        distance = inputtxt.get("1.0", "end-1c")
        try:
            distance = int(distance)
        except ValueError:
            messagebox.showinfo("Error", "You can only input a number in the distance field.")
    def ExportFindings():
        print("nog niet geimplementeerd.")

    def placeComment():
        global commentsDict
        time = timeText.get("1.0", "end-1c")
        comment = commentText.get("1.0", "end-1c")
        #print(str(manoutils.validateTime(time))+ " " + time+ " "+ comment)
        if manoutils.validateTime(time):
            commentsDict[manoutils.convertTime(time)] = comment
        else:
            messagebox.showinfo("Error", "You must enter the right format of time (HH:MM:SS)")

    root = tk.Tk()
    root.title("ManoMap Remake")

    # Create  frames
    fileName_frame = tk.Frame(root, relief="ridge", borderwidth=2)
    sensors_frame = tk.Frame(root, relief="ridge", borderwidth=2)
    settings_frame = tk.Frame(root, relief="ridge", borderwidth=2)
    data_frame = tk.Frame(root, relief="ridge", borderwidth=2)

    # Place the frames in the root window
    fileName_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
    sensors_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    settings_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
    data_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

    # Configure columns to take 30% of screen width each
    root.columnconfigure(0, weight=1)  # 30%
    root.columnconfigure(1, weight=1)  # 30%
    root.columnconfigure(2, weight=1)  # 30%


    #filename frame
    fileTitle = tk.StringVar()

    fileLabel = tk.Label(fileName_frame, textvariable=fileTitle)
    fileTitle.set("No file selected")
    fileLabel.pack(side=tk.TOP)

    # Sensors frame
    sensor_title = tk.StringVar()
    label = tk.Label(sensors_frame, textvariable=sensor_title, font=("Helvetica", 16, "underline"))
    sensor_title.set("Sensors")
    label.pack()

    var = tk.StringVar()
    label = tk.Label(sensors_frame, textvariable=var)
    var.set("Visible sensors:")
    label.pack(side=tk.TOP)

    hVar1 = tk.DoubleVar(value=1)
    hVar2 = tk.DoubleVar(value=40)
    visibleSensorSlider = RangeSliderH(sensors_frame, [hVar1, hVar2], Width=400, Height=65, padX=15, min_val=1, max_val=40, show_value=True, step_size=1, bar_radius=5, digit_precision='.0f')
    visibleSensorSlider.pack()

    distanceText = tk.StringVar()
    label = tk.Label(sensors_frame, textvariable=distanceText)
    distanceText.set("Distance between sensors: (cm)")
    label.pack()

    inputtxt = tk.Text(sensors_frame, height=1, width=30)
    inputtxt.pack()

    colonRegionsText = tk.StringVar()
    label = tk.Label(sensors_frame, textvariable=colonRegionsText)
    colonRegionsText.set("ColonRegions: ")
    label.pack()

    ascendingMin = tk.DoubleVar(value=1)
    ascendingMax = tk.DoubleVar(value=10)
    transverseMin = tk.DoubleVar(value=11)
    transverseMax = tk.DoubleVar(value=20)
    descendingMin = tk.DoubleVar(value=21)
    descendingMax = tk.DoubleVar(value=30)
    sigmoidMin = tk.DoubleVar(value=31)
    sigmoidMax = tk.DoubleVar(value=37)
    rectumMin = tk.DoubleVar(value=38)
    rectumMax = tk.DoubleVar(value=40)


    var = tk.StringVar()
    label = tk.Label(sensors_frame, textvariable=var)
    var.set("Ascending:")
    label.pack()
    ascendingMin = tk.DoubleVar(value=1)
    ascendingMax = tk.DoubleVar(value=10)
    ascendingSensorSlider = RangeSliderH(sensors_frame, [ascendingMin, ascendingMax], Width=400, Height=55, padX=15, min_val=1, max_val=40, show_value=True, step_size=1, bar_radius=5, digit_precision='.0f')

    ascendingSensorSlider.pack()


    var = tk.StringVar()
    label = tk.Label(sensors_frame, textvariable=var)
    var.set("Transverse:")
    label.pack()
    transverseMin = tk.DoubleVar(value=11)
    transverseMax = tk.DoubleVar(value=20)
    transverseSensorSlider = RangeSliderH(sensors_frame, [transverseMin, transverseMax], Width=400, Height=55, padX=15, min_val=1, max_val=40, show_value=True, step_size=1, bar_radius=5, digit_precision='.0f')

    transverseSensorSlider.pack()

    var = tk.StringVar()
    label = tk.Label(sensors_frame, textvariable=var)
    var.set("Descending:")
    label.pack()

    descendingMin = tk.DoubleVar(value=21)
    descendingMax = tk.DoubleVar(value=30)
    descendingSensorSlider = RangeSliderH(sensors_frame, [descendingMin, descendingMax], Width=400, Height=55, padX=15, min_val=1, max_val=40, show_value=True, step_size=1, bar_radius=5, digit_precision='.0f')

    descendingSensorSlider.pack()


    var = tk.StringVar()
    label = tk.Label(sensors_frame, textvariable=var)
    var.set("Sigmoid:")
    label.pack()
    sigmoidMin = tk.DoubleVar(value=31)
    sigmoidMax = tk.DoubleVar(value=35)
    sigmoidSensorSlider = RangeSliderH(sensors_frame, [sigmoidMin, sigmoidMax], Width=400, Height=55, padX=15, min_val=1, max_val=40, show_value=True, step_size=1, bar_radius=5, digit_precision='.0f')

    sigmoidSensorSlider.pack()

    var = tk.StringVar()
    label = tk.Label(sensors_frame, textvariable=var)
    var.set("Rectum:")
    label.pack()
    rectumMin = tk.DoubleVar(value=36)
    rectumMax = tk.DoubleVar(value=40)
    rectumSensorSlider = RangeSliderH(sensors_frame, [rectumMin, rectumMax], Width=400, Height=55, padX=15, min_val=1, max_val=40, show_value=True, step_size=1, bar_radius=5, digit_precision='.0f')

    rectumSensorSlider.pack()

    # settings frame
    settings_title = tk.StringVar()
    label = tk.Label(settings_frame, textvariable=settings_title, font=("Helvetica", 16, "underline"))
    settings_title.set("Settings")
    label.pack()

    thresholdText = tk.StringVar()
    label = tk.Label(settings_frame, textvariable=thresholdText)
    thresholdText.set("Thresholds:")
    label.pack()

    def forceSlider(name):
        if name == "ascending":
            ascendingSensorSlider.forceValues([ascendingMin.get(), ascendingMax.get()])
            return
        if name == "transverse":
            transverseSensorSlider.forceValues([transverseMin.get(), transverseMax.get()])
            return
        if name == "descending":
            descendingSensorSlider.forceValues([descendingMin.get(), descendingMax.get()])
            return
        if name == "sigmoid":
            sigmoidSensorSlider.forceValues([sigmoidMin.get(), sigmoidMax.get()])
            return
        if name == "rectum":
            rectumSensorSlider.forceValues([rectumMin.get(), rectumMax.get()])
            return
        raise NameError("Not a valid name for a colon region")

    def adjustSlider(i):
        if i == 0 or i == 9:
            return
        doublevars = [ascendingMin, ascendingMax, transverseMin, transverseMax, descendingMin, descendingMax,
                      sigmoidMin, sigmoidMax, rectumMin, rectumMax]
        if i % 2 == 0:
            doublevars[i-1].set(doublevars[i].get() - 1)
        else:
            if i < 9:
                doublevars[i+1].set(doublevars[i].get() + 1)
        if i < 2:
            forceSlider("ascending")
            return
        if i < 4:
            forceSlider("transverse")
            return
        if i < 6:
            forceSlider("descending")
            return
        if i < 8:
            forceSlider("sigmoid")
            return
        if i < 10:
            forceSlider("rectum")
            return

    def adjustSliderWrapper(index):
        def out(a,b,c):
            adjustSlider(index)
        return out

    ascendingMin.trace("w", adjustSliderWrapper(0))
    ascendingMax.trace("w", adjustSliderWrapper(1))
    transverseMin.trace("w", adjustSliderWrapper(2))
    transverseMax.trace("w", adjustSliderWrapper(3))
    descendingMin.trace("w", adjustSliderWrapper(4))
    descendingMax.trace("w", adjustSliderWrapper(5))
    sigmoidMin.trace("w", adjustSliderWrapper(6))
    sigmoidMax.trace("w", adjustSliderWrapper(7))
    rectumMin.trace("w", adjustSliderWrapper(8))
    rectumMax.trace("w", adjustSliderWrapper(9))

    hVar3 = tk.DoubleVar(value=10)
    hVar4 = tk.DoubleVar(value=200)

    thresholdSlider = RangeSliderH(settings_frame, [hVar3, hVar4], Height=65, padX=20, min_val=0, max_val=500, show_value=True, step_size=5, bar_radius=5, digit_precision='.0f')
    thresholdSlider.pack()

    analysisStartTime = tk.StringVar()
    label = tk.Label(settings_frame, textvariable=analysisStartTime)
    analysisStartTime.set("Start time of analysis (HH:MM:SS):")
    label.pack()
    startTimeText = tk.Text(settings_frame, height=1, width=30)
    startTimeText.pack()

    timecommentBundle = tk.Frame(settings_frame)
    timecommentBundle.pack(padx=20, pady=20)
    timeAndCommentText = tk.StringVar()
    label = tk.Label(timecommentBundle, textvariable=timeAndCommentText)
    timeAndCommentText.set("Time & Comment: (HH:MM:SS)")
    label.pack()
    timeText = tk.Text(timecommentBundle, height=1, width=10)
    timeText.pack(side=tk.LEFT)
    commentText = tk.Text(timecommentBundle, height=1, width=50)
    commentText.pack(side=tk.RIGHT)

    placeCommentButton = tk.Button(settings_frame, text="Place Comment", command=placeComment)
    placeCommentButton.pack(pady=10, padx=10)

    options = [
        "inferno",
        "hot",
        "Greys",
    ]

    clicked = tk.StringVar()
    clicked.set("inferno")

    drop = tk.OptionMenu(settings_frame, clicked, *options)
    drop.pack(pady=10, padx=10)


    # data frame
    data_title = tk.StringVar()
    label = tk.Label(data_frame, textvariable=data_title, font=("Helvetica", 16, "underline"))
    data_title.set("Data")
    label.pack()


    file_button = tk.Button(data_frame, text="Select Input File", command=openFile)
    file_button.pack(side=tk.TOP, padx=10, pady=10)


    plotButton = tk.Button(data_frame, text="Plot Data", command=showPlotPressed)
    plotButton.pack(pady=10, padx=10)

    signalButton = tk.Button(data_frame, text="Plot signals", command=showSignalsPressed)
    signalButton.pack(pady=10, padx=10)

    detectButton = tk.Button(data_frame, text="Detect Events", command=detectEventsPressed)
    detectButton.pack(pady=10, padx=10)

    exportButton = tk.Button(data_frame, text="ExportData", command=ExportFindings)
    exportButton.pack(pady=10, padx=10)

    root.mainloop()

"""
🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀
🐀             CRAZY?               🐀
🐀     ...I WAS CRAZY ONCE...       🐀
🐀  ...THEY LOCKED ME IN A ROOM...  🐀
🐀      ...A RUBBER ROOM...         🐀
🐀  ...A RUBBER ROOM WITH RATS...   🐀
🐀   ...AND RATS MAKE ME CRAZY!!!!  🐀
🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀🐀
"""
if __name__ == '__main__':
    main()
