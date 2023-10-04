import matplotlib.pyplot as plt
import numpy as np
import manoutils




def show_combined_plot(valuesDict, commentsDict, first_sensor, last_sensor, minThreshold, maxThreshold, opacity=1, colormap='inferno', detected_events=""):
    data = valuesDict
    granulariteit = manoutils.get_granularity_factor()

    x_values = list(data.keys())
    tmp = []
    for val in x_values:
        tmp.append(val*granulariteit)
    x_values = tmp
    amount_of_sensors = last_sensor - first_sensor + 1
    y_offset = 100
    y_offset2 = y_offset
    scaling_factor = 0.1
    plt.figure().set_figheight(10.0)
    laatste_kleur =0.1
    for x in range(amount_of_sensors):
        y_values = [
            y_offset if value[x] < minThreshold else (value[x] - minThreshold) * scaling_factor + y_offset
            for value in data.values()
        ]
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

    for entry in commentsDict:
        print(tick_locations[0])
        plt.annotate(commentsDict[entry], xy=(entry, tick_locations[0]*-5 +140), xytext=(entry + 1, tick_locations[0]*-5 +140),color='black')
    #detected_events = [[3265,11,{'sensors': [13, 14, 15], 'matches': [13, 14, 15]}],
     #                  [4320,16,{'sensors': [23, 24, 25], 'matches': [23, 24, 25]}]]
    if detected_events != "":
        for item in detected_events:
            row = item[0]
            length  = item[1]
            matchdict = item[2]
            sensors = matchdict["sensors"]
            matches = matchdict["matches"]
            firstCounter = 0
            lastCounter = -1
            smallest_common= sensors[firstCounter]
            biggest_common=sensors[lastCounter]
            while smallest_common not in matches:
                firstCounter +=1
                smallest_common = sensors[firstCounter]
            while biggest_common not in matches:
                lastCounter -=1
                biggest_common = sensors[lastCounter]
            x1 = row* granulariteit/10
            #x1 = row/manoutils.get_granularity_factor()

            y1 = (smallest_common -1)*scaling_factor + (y_offset2 - (5*(smallest_common)))
            plt.scatter(x1, y1, color = 'red', label='begin point')
            x2 = (row + length) *granulariteit/10
            #x2 = (row + length)/manoutils.get_granularity_factor()

            y2 = (biggest_common-1)*scaling_factor + (y_offset2 - (5*(biggest_common) ))
            plt.scatter(x2, y2, color='blue', label = 'end_point')
            print("smallest_common:", smallest_common, "biggest_common:", biggest_common)
            print("coordinaten", x1, y1, x2, y2)
            line_coefficient = (y2 - y1) / (x2 - x1)
            if line_coefficient > 0:
                line_color = 'green'
            else:
                line_color = 'yellow'
            plt.plot([x1, x2], [y1, y2], color=line_color, linestyle='--')

        ##########HIER NU PUNT PLOTTEN VOOR ROW SMALLEST SENSOR, ROW + LENGTH BIGGEST COMMON

    plt.show()

