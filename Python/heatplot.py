import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import manoutils

#Toont plot in matplotlib nieuwe window. Kan naar externe module gerefactord worden
def showPlot(firstSensor, lastSensor, minThreshold, maxThreshold, differentialMode, valuesDict, commentsDict, colormap='inferno', smoothing_strength = 1):
    matplotlib.pyplot.close('all')
    #only shows values between first and last sensor ADDS AN EMPTY LINE BEFORE DATA
    p = manoutils.dictionary_to_ndarray(valuesDict)[firstSensor:lastSensor+1]
    l = np.array([[0 for el in p[1]]])
    p = np.vstack((l, p))

    minT = minThreshold
    maxT = maxThreshold
    cmap = colormap

    for entry in commentsDict:
        plt.annotate(commentsDict[entry], xy=(entry, firstSensor), xytext=(entry + 1, firstSensor),color='black')

    if smoothing_strength > 1:
        manoutils.smooth_ndArray(p, 5)

    #als differentialMode aan staat, toon het verschil ten opzichte van vorige waarde ipv de waarde zelf.
    if differentialMode:
        minT = -3
        maxT = 3
        cmap = 'coolwarm'
        p = manoutils.calculate_differences(p)
    tmp = plt.imshow(p, cmap=cmap, interpolation='none', aspect='auto', vmin=minT, vmax=maxT)
    plt.yticks(np.arange(firstSensor, lastSensor +1, 1))
    plt.axis([0, len(list(valuesDict)), lastSensor, firstSensor])
    plt.colorbar(tmp)
    plt.show()
