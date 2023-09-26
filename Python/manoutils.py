import csv
import numpy as np

#Functie die CSV (of txt mits juiste syntax) file path input neemt en een dictionary returnt. Timestamps zijn keys.

def CSVToDict(file):
    out = dict()
    with open(file) as csvfile:
        rdr = csv.reader(csvfile, delimiter=' ', quotechar='|')
        rownumber = 1
        for row in rdr:
            rownumber+=1
            if rownumber % 10 != 0:
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
