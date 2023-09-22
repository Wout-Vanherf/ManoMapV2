import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import manoutils

#Toont plot in matplotlib nieuwe window. Kan naar externe module gerefactord worden
def showPlot(firstSensor, lastSensor, minThreshold, maxThreshold, differentialMode, valuesDict, colormap='inferno', smoothing_strength = 1):
    matplotlib.pyplot.close('all')
    p = manoutils.dictionary_to_ndarray(valuesDict)

    minT = minThreshold
    maxT = maxThreshold
    cmap = colormap
    #te veel performance loss

    if smoothing_strength > 1:
        manoutils.smooth_ndArray(p, 5)

    #als differentialMode aan staat, toon het verschil ten opzichte van vorige waarde ipv de waarde zelf.
    if differentialMode:
        minT = -3
        maxT = 3
        cmap = 'coolwarm'
        p = manoutils.calculate_differences(p)
    tmp = plt.imshow(p, cmap=cmap, interpolation='none', aspect='auto', vmin=minT, vmax=maxT)
    plt.yticks(np.arange(firstSensor, lastSensor + 1, 2))
    plt.axis([0, len(list(valuesDict)), lastSensor, firstSensor])
    cb = plt.colorbar(tmp)
    plt.show()
