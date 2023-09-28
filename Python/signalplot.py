import matplotlib.pyplot as plt
import numpy as np
import manoutils




def show_combined_plot(valuesDict, first_sensor, last_sensor, minThreshold, maxThreshold, smoothing_strength=1, opacity=1, colormap='inferno'):

    data = valuesDict

    x_values = list(data.keys())
    amount_of_sensors = last_sensor - first_sensor + 1
    y_offset = 100

    plt.figure().set_figheight(10.0)
    laatste_kleur =0.1
    for x in range(amount_of_sensors):
        scaling_factor = 0.1

        #Eigenlijk zou het zo moeten doen maar dit macheert nog nie, zoda we de filter kunnen doen voordat we de threshold applyen, anders zitten we tereug met negatieve waarden.
        y_values = [(value[x] - minThreshold) * scaling_factor + y_offset for value in data.values()]
        for i, val in enumerate(y_values):
            if val < minThreshold:
                y_values[i] = y_offset


        y_values = [
            y_offset if value[x] < minThreshold else (value[x] - minThreshold) * scaling_factor + y_offset
            for value in data.values()
        ]

        if smoothing_strength > 1:
            y_values = manoutils.smooth_row(y_values, smoothing_strength)


        graphColor = plt.get_cmap(colormap)(laatste_kleur)
        graphColor = (graphColor[0],graphColor[1],graphColor[2], opacity)
        if colormap == "Greys":
            graphColor=(0.3,0.3,0.3, opacity)
        plt.plot(x_values, y_values, label='sensor ' + str(x), linewidth=0.5, color= graphColor)
        y_offset -= 5  # Increment Y offset for the next sensor
        laatste_kleur+= 1/(amount_of_sensors + 30)

    plt.xlabel('time (deciseconden)', fontsize=10)
    plt.ylabel('Sensor Number', fontsize=10)
    plt.xticks(fontsize=8)
# Adjust the y-axis ticks with custom tick locations and labels
    if(first_sensor==0):
        tick_locations = np.arange(1, amount_of_sensors + 1)
        tick_labels = [str(i + first_sensor) for i in tick_locations]  # Convert tick locations to string labels
    else:
        tick_locations = np.arange(1, amount_of_sensors + 1)
        tick_labels = [str(i + first_sensor -1 ) for i in tick_locations]

    plt.yticks(tick_locations*-5 +105 , tick_labels, fontsize=8)
    plt.xlim(0, x_values[-1])  # Set the x-axis limits

    plt.gca().set_aspect('auto', adjustable='box')

    plt.show()

