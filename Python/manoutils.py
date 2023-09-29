import csv
import numpy as np
from scipy.signal import savgol_filter

granularity_factor = 100

def get_granularity_factor():
    return granularity_factor

#Functie die CSV (of txt mits juiste syntax) file path input neemt en een dictionary returnt. Timestamps zijn keys.
def CSVToDict(file):
    out = dict()
    with open(file) as csvfile:
        rdr = csv.reader(csvfile, delimiter=' ', quotechar='|')
        rownumber = 1
        for row in rdr:
            rownumber+=1
            if rownumber % granularity_factor != 0:
                continue
            if rownumber < 10:
                continue
            rowToAdd = []
            for val in row[1:]:
                try:
                    currentVal = int(val.strip().replace(',', ''))
                except:
                    currentVal = float(val.strip().replace(',', ''))
                rowToAdd.append(currentVal)
            out[rownumber] = rowToAdd
    return out

def calculate_differences(arr):
    num_rows, num_cols = len(arr), len(arr[0])
    result = []
    for row in arr:
        new_row = [row[0]]
        for i in range(1, num_cols):
            difference = row[i] - row[i - 1]
            new_row.append(difference)
        result.append(new_row)
    return result

def average(arr):
    out = 0
    for i in arr:
        out += i
    return out/len(arr)

def smooth_row(arr, filter_length):
    out = []
    for i in range(len(arr)):
        lowerBound = max(0, i-filter_length)
        upperBound = min(len(arr)-1, i+filter_length)
        out.append(average(arr[lowerBound:upperBound]))
    return out

def smooth_ndArray(ndarr, filterLength):
    out = []
    for row in ndarr:
        out.append(smooth_row(row, filterLength))
    return np.array(out)

#zet een dictionary om naar een 2D Numpy Array (gebruikt om te plotten, row 1 = sensor 1 etc...) 🐀
def dictionary_to_ndarray(data_dict):
    values = list(data_dict.values())
    nd_array = np.stack(values)
    return nd_array.transpose()

# valideer time fields
def validateTime(input):
    try:
        parts = input.split(":")
    except:
        return False
    if len(parts) != 3:
        return False
    try:
        hours, minutes, seconds = map(int, parts)
        if 0 <= hours <= 23 and 0 <= minutes <= 59 and 0 <= seconds <= 59:
            return True
    except ValueError:
        pass
    return False

#convert HH:MM:SS naar  x deciseconden
def convertTime(input):
    parts = input.split(":")
    total = 0
    try:
        total = int(parts[0])*60
        total = (total + int(parts[1])) * 60
        total = (total + int(parts[2])) * 10
    except:
        print("fout in omzetten")
    return total

def savgol_smooth(data, window_size, po=1):
    return savgol_filter(data, window_length=window_size, polyorder=po)

def savgol_smooth_ndArray(arr, window_size, po=1):
    out = []
    for row in arr:
        val = savgol_smooth(row, window_size, po)
        out.append(val)
    return np.array(out)


def transform_dict_per_timeframe_to_per_sensor(dict):
    new_dict = {}
    list_length = len(next(iter(dict.values())))
    for i in range(1, list_length + 1):
        new_key = i
        new_value = []
        for key, value in dict.items():
            new_value.append(value[i - 1])
            new_dict[new_key] = new_value
    return new_dict

def transform_dict_per_sensor_to_dict_per_timeframe(dict, timeframe = 0.1):
    new_dict = {}
    list_length = len(next(iter(dict.values())))
    for i in range(1, list_length + 1):
        #new_key = i * timeframe - timeframe
        new_key = round(i * timeframe - timeframe, 10)
        new_value = []
        for key, value in dict.items():
            new_value.append(value[i - 1])
            new_dict[new_key] = new_value
    return new_dict

#time in sec

