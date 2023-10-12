import matplotlib.pyplot as plt
import numpy as np
import manoutils

def ysort(xvals, yvals):
    if len(xvals) != len(yvals):
        raise ValueError("Dimension mismatch")
    tmp = []
    for i in range(len(xvals)):
        tmp.append((xvals[i], yvals[i]))
    tmp = sorted(tmp, key=lambda val: val[1])
    tmp_xvals = []
    tmp_yvals = []
    for val in tmp:
        tmp_xvals.append(val[0])
        tmp_yvals.append(val[1])
    return tmp_xvals, tmp_yvals


def cubic_bezier(t, control_points):
    n = len(control_points)
    result = 0
    for i in range(len(control_points)):
        result += control_points[i] * np.math.comb(n - 1, i) * (1 - t) ** (n - 1 - i) * t ** i
    return result

def draw_direct(xvals, yvals):
    for i in range(len(xvals[:-1])):
        x_values = [xvals[i], xvals[i+1]]
        y_values = [yvals[i], yvals[i+1]]
        plt.plot(x_values, y_values, "b", linestyle="--")



def draw_bezier(x_values, y_values):
    if len(x_values) < 2:
        return
    t_values = np.linspace(0, 1, 100)
    curve_x = []
    curve_y = []
    for t in t_values:
        curve_x.append(cubic_bezier(t, x_values))
        curve_y.append(cubic_bezier(t, y_values))
    plt.plot(curve_x, curve_y, color='blue', linestyle='--')

def show_combined_plot(valuesDict, commentsDict, first_sensor, last_sensor, minThreshold, maxThreshold, opacity=1, colormap='inferno', detected_events="", draw_method="bezier"):
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
    offsets_per_sensor = {}
    for x in range(amount_of_sensors):
        offsets_per_sensor[x]= y_offset
        y_values = []
        for value in data.values():
            if value[x] < minThreshold:
                y_value = y_offset
            else:
                y_value = (value[x] - minThreshold) * scaling_factor + y_offset
            y_values.append(y_value)
        graphColor = plt.get_cmap(colormap)(laatste_kleur)
        graphColor = (graphColor[0],graphColor[1],graphColor[2], opacity)
        if colormap == "Greys":
            graphColor=(0.3,0.3,0.3, opacity)
        plt.plot(x_values, y_values, label='sensor ' + str(x), linewidth=0.5, color= graphColor)
        y_offset -= 5  # Increment Y offset for the next sensor
        laatste_kleur+= 1/(amount_of_sensors + 30)
    #print("offsets_per_sensor", offsets_per_sensor)
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
        #print(tick_locations[0])
        x_position = entry / manoutils.get_granularity_factor()
        y_position = 1  # Adjust the y-position as needed to place comments above the heatmap
        annotation_text = commentsDict[entry]
        plt.annotate(annotation_text, xy=(0,0), xytext=(x_position, tick_locations[0]*-5 +140),color='black')
        #plt.annotate(commentsDict[entry], xy=(entry, tick_locations[0]*-5 +140), xytext=(entry + 1, tick_locations[0]*-5 +140),color='black')

    if detected_events != "":
        for contraction in detected_events:
            pressure_per_sensor_dict = {}
            contraction_length = contraction["length"]
            measurement_number = contraction["measure_number"]
            sequence_counter = 0
            for sequence in contraction["sequences"]:
                sequence_counter +=1
                for value_pair in sequence:

                    sensor_number = value_pair[0]
                    pressure_data = value_pair[1]
                    if sensor_number not in pressure_per_sensor_dict.keys():
                        pressure_per_sensor_dict[sensor_number] = {}
                        pressure_per_sensor_dict[sensor_number][sequence_counter] = pressure_data
                    else:
                        pressure_per_sensor_dict[sensor_number][sequence_counter] = pressure_data
            #print("pressure_per_sensor_dict: ", pressure_per_sensor_dict)
            max_pressure_per_sensor_with_counter = {}
            for sensor, measurements in pressure_per_sensor_dict.items():
                max_pressure = max(measurements.values())
                max_sequence_number = max(measurements, key=measurements.get)
                max_pressure_per_sensor_with_counter[sensor] = [max_pressure, max_sequence_number]

            #print("max_pressure_per_sensor_with_counter: ",max_pressure_per_sensor_with_counter)
            #plot all max pressure points.
            x_values = []
            y_values = []
            for sensor in max_pressure_per_sensor_with_counter:
                max_pressure, max_sequence_number = max_pressure_per_sensor_with_counter[sensor]
                #print("sensor:", sensor, "max_pressure: ",max_pressure,"max_sequence_number: ", max_sequence_number)

                x = (measurement_number + max_sequence_number) * granulariteit * scaling_factor - granulariteit*scaling_factor
                y = (max_pressure - minThreshold) * scaling_factor + offsets_per_sensor[sensor -1]
                #print("x: ", x, "y:", y)
                x_values.append(x)
                y_values.append(y)

                plt.scatter(x, y, color= 'red',marker ='x')

            x_values,y_values = ysort(x_values, y_values)
            if draw_method == "bezier":
                draw_bezier(x_values, y_values)
            if draw_method == "direct":
                draw_direct(x_values, y_values)

    plt.show()






        ##########HIER NU PUNT PLOTTEN VOOR ROW SMALLEST SENSOR, ROW + LENGTH BIGGEST COMMON



