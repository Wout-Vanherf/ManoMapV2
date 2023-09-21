import csv
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename


def inferno_color(value):
    inferno_cmap = plt.get_cmap("inferno")
    color = inferno_cmap(value)
    return (color[0],color[1],color[2],0.8)

def show_combined_plot(valuesDict):

    data = valuesDict

    x_values = list(data.keys())
    amount_of_sensors = 40
    y_offset = 100  # Starting Y value for the first sensor

    # Create a single subplot
    plt.figure().set_figheight(10.0)  # Adjust figure height to fit all sensors
    laatste_kleur =0.1
    for x in range(amount_of_sensors):
        scaling_factor = 0.1 #compression of the values on the y scale to make them more compact

        y_values = [values[x]* scaling_factor + y_offset for values in data.values()]
        plt.plot(x_values, y_values, label='sensor ' + str(x), linewidth=0.5, color= inferno_color(laatste_kleur))
        y_offset -= 5  # Increment Y offset for the next sensor
        laatste_kleur+= 1/(amount_of_sensors + 30)

    plt.xlabel('time (deciseconden)', fontsize=10)
    plt.ylabel('Sensor Number', fontsize=10)
    plt.xticks(fontsize=8)
# Adjust the y-axis ticks with custom tick locations and labels
    tick_locations = np.arange(1, amount_of_sensors + 1)
    tick_labels = [str(i) for i in tick_locations]  # Convert tick locations to string labels

    plt.yticks(tick_locations*-5 +105 , tick_labels, fontsize=8)
    plt.xlim(0, x_values[-1])  # Set the x-axis limits

    plt.gca().set_aspect('auto', adjustable='box')
    #plt.legend()  # Add a legend to distinguish the sensors

    plt.show()

