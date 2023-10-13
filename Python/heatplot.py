import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import manoutils

#Toont plot in matplotlib nieuwe window. Kan naar externe module gerefactord worden
def showPlot(firstSensor, lastSensor, minThreshold, maxThreshold, differentialMode, valuesDict, commentsDict, colormap='inferno', smoothing_strength=1):
    plt.close('all')
    # Only shows values between first and last sensor, ADDS AN EMPTY LINE BEFORE DATA
    p = manoutils.dictionary_to_ndarray(valuesDict)[firstSensor:lastSensor + 1]
    print(p)
    l = np.array([[0 for _ in p[1]]])
    for i in "12":
        p = np.vstack((l, p)) #NIET AANRAKEN MAN IS CURSED, ECHT WAAR GELOOF MIJ SHIT GAAT BREKEN

    minT = minThreshold
    maxT = maxThreshold
    cmap = colormap

    if smoothing_strength > 1:
        manoutils.smooth_ndArray(p, 5)

    # If differentialMode is on, show the difference relative to the previous value
    if differentialMode:
        minT = -3
        maxT = 3
        cmap = 'coolwarm'
        p = manoutils.calculate_differences(p)

    fig, ax1 = plt.subplots()

    # Create the heatmap
    tmp = ax1.imshow(p, cmap=cmap, interpolation='none', aspect='auto', vmin=minT, vmax=maxT)
    ax1.set_yticks(np.arange(firstSensor, lastSensor + 1, 1))
    ax1.set_xlim(0, len(list(valuesDict)))
    ax1.set_ylim(lastSensor, firstSensor)

    # Create a twin axis for the comments (on top of the original heatmap)
    ax2 = ax1.twinx()

    # Create the timeline with comments on the top axis
    for entry in commentsDict:
        x_position = entry / manoutils.get_granularity_factor()
        y_position = 1  # Adjust the y-position as needed to place comments above the heatmap
        annotation_text = commentsDict[entry]
        ax2.annotate(annotation_text, xy=(x_position, y_position), xytext=(x_position + 1, y_position),
                     color='red', fontsize=8, ha='left', va='bottom', rotation=0)

    cb = plt.colorbar(tmp)
    plt.show()
