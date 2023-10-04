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
    print("offsets_per_sensor", offsets_per_sensor)
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
    """"
    detected_events = [{'length': 36, 'measure_number': 864, 'sequences': [
        [(24, 20.611), (25, 65.909), (26, 11.901)],
        [(23, 10.251), (24, 20.783), (25, 47.773), (26, 21.888)],
        [(23, 13.011), (24, 21.229), (25, 44.685), (26, 29.569), (27, 10.575)],
        [(21, 14.011), (22, 10.4), (23, 15.469), (24, 20.611), (25, 33.74), (26, 34.697), (27, 27.858), (28, 17.981)],
        [(14, 15.379), (15, 10.983), (16, 10.949), (17, 10.994), (18, 12.531), (19, 12.383), (20, 11.783), (21, 15.817), (22, 12.263), (23, 15.246), (24, 18.303), (25, 28.41), (26, 37.172), (27, 41.709), (28, 51.279), (29, 24.459), (30, 28.763), (31, 47.9)],
        [(14, 15.697), (15, 10.893), (16, 10.549), (17, 10.594), (18, 13.057), (19, 12.309), (20, 11.869), (21, 15.617), (22, 12.829), (23, 14.72), (24, 15.549), (25, 19.371), (26, 35.192), (27, 36.277), (28, 54.472), (29, 29.959), (30, 41.449), (31, 50.166), (32, 40.213)],
        [(18, 11.731), (19, 10.634), (20, 10.337), (21, 13.047), (22, 12.24), (23, 15.823), (24, 13.68), (25, 20.252), (26, 23.176), (27, 24.071), (28, 35.298), (29, 20.758), (30, 34.348), (31, 38.793), (32, 87.595)],
        [(25, 19.559), (26, 23.669), (27, 16.186), (28, 12.656), (29, 10.294), (30, 21.008), (31, 22.54), (32, 86.434)],
        [(25, 18.674), (26, 18.829), (27, 15.734), (28, 17.72)],
        [(25, 20.689), (26, 18.989), (27, 13.734), (28, 15.736), (29, 10.257), (30, 19.623), (31, 16.717), (32, 33.395)],
        [(24, 10.684), (25, 17.022), (26, 17.474), (27, 13.871), (28, 17.193), (29, 10.503), (30, 18.571), (31, 18.604), (32, 29.056)],
        [(25, 11.396), (26, 14.034), (27, 13.957), (28, 17.291), (29, 10.72), (30, 17.75), (31, 24.259), (32, 24.149)],
        [(24, 39.869), (25, 13.451), (26, 13.189), (27, 14.134), (28, 17.091), (29, 10.897), (30, 16.198), (31, 29.195), (32, 23.971)],
        [(24, 107.911), (25, 14.435), (26, 14.829), (27, 13.911), (28, 17.022), (29, 11.057), (30, 15.543), (31, 33.124), (32, 25.589)],
        [(24, 124.648), (25, 15.469), (26, 14.497), (27, 13.968), (28, 17.885), (29, 11.166), (30, 14.926), (31, 35.51), (32, 29.331)],
        [(24, 65.407), (25, 14.96), (26, 13.713), (27, 14.077), (28, 18.411), (29, 11.251), (30, 14.629), (31, 37.823), (32, 32.691)],
        [(26, 12.954), (27, 14.3), (28, 18.662), (29, 11.12), (30, 14.92), (31, 39.349), (32, 34.657)],
        [(26, 11.877), (27, 14.362), (28, 18.931), (29, 11.086), (30, 15.166), (31, 40.274), (32, 35.531)],
        [(26, 10.583), (27, 14.465), (28, 19.371), (29, 11.0), (30, 15.383), (31, 41.097), (32, 35.646)],
        [(27, 14.362), (28, 18.862), (29, 10.651), (30, 15.417), (31, 41.411), (32, 35.457)],
        [(27, 13.98), (28, 18.228), (29, 10.423), (30, 15.737), (31, 41.909), (32, 36.069)],
        [(27, 13.465), (28, 17.662), (29, 10.263), (30, 16.297), (31, 42.766), (32, 37.497)],
        [(27, 13.265), (28, 17.776), (29, 10.274), (30, 16.8), (31, 43.577), (32, 38.834)],
        [(26, 10.234), (27, 13.345), (28, 17.525), (29, 10.08), (30, 17.337), (31, 44.371), (32, 39.731)],
        [(26, 11.606), (27, 13.431), (28, 17.411)],
        [(26, 11.8), (27, 13.414), (28, 17.399)],
        [(26, 11.989), (27, 13.431), (28, 17.971)],
        [(26, 11.474), (27, 13.362), (28, 18.148)],
        [(25, 10.103), (26, 10.943), (27, 13.214), (28, 17.971)],
        [(25, 12.731), (26, 11.794), (27, 13.3), (28, 17.822), (29, 10.069), (30, 22.017), (31, 46.343), (32, 41.074)],
        [(25, 13.623), (26, 13.503), (27, 13.831), (28, 17.748), (29, 10.503), (30, 22.229), (31, 44.423), (32, 41.271), (33, 16.696)],
        [(25, 12.749), (26, 13.874), (27, 14.26), (28, 17.251), (29, 10.749), (30, 21.789), (31, 43.316), (32, 29.991), (33, 18.727)],
        [(25, 12.771), (26, 16.017), (27, 14.3), (28, 16.622), (29, 10.754), (30, 21.391), (31, 39.085), (32, 25.646), (33, 16.439)],
        [(25, 12.411), (26, 16.276), (27, 14.282), (28, 16.873), (29, 10.686), (30, 20.425), (31, 36.965), (32, 30.243)],
        [(25, 11.937), (26, 20.328), (27, 14.311), (28, 17.359), (29, 10.617), (30, 20.349), (31, 37.057), (32, 40.403)],
        [(25, 10.549), (26, 25.076), (27, 13.962), (28, 17.388), (29, 10.2), (30, 20.762), (31, 37.917), (32, 39.949)]]}
                       ]
    """
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
            y_values =  []
            for sensor in max_pressure_per_sensor_with_counter:
                max_pressure, max_sequence_number = max_pressure_per_sensor_with_counter[sensor]
                print("sensor:", sensor, "max_pressure: ",max_pressure,"max_sequence_number: ", max_sequence_number)

                x = (measurement_number + max_sequence_number) * granulariteit * scaling_factor - granulariteit*scaling_factor
                y = (max_pressure - minThreshold) * scaling_factor + offsets_per_sensor[sensor -1]
                #print("x: ", x, "y:", y)
                x_values.append(x)
                y_values.append(y)
                plt.scatter(x, y, color = 'red',marker ='x')
                """"
            #polyfit voor de coefficient van de best-fit-line
            coefficient = np.polyfit(x_values, y_values, 1)
            best_fit_line = np.poly1d(coefficient)
            x_fit = np.linspace(min(x_values), max(x_values), 10)
            y_fit = best_fit_line(x_fit)
            plt.plot(x_fit, y_fit, color="pink", linestyle='-', label='Best Fit Line')
            """

    plt.show()







""""
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
        """
        ##########HIER NU PUNT PLOTTEN VOOR ROW SMALLEST SENSOR, ROW + LENGTH BIGGEST COMMON



