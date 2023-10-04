import random

import numpy as np
import matplotlib.pyplot as plt
import manoutils
from scipy.signal import morlet
from matplotlib.animation import FuncAnimation

# Parameters
freq = 1
width = 500
t = np.linspace(-5 * np.pi, 5 * np.pi, width)

# Initialize the figure and axis
fig, ax = plt.subplots(figsize=(10, 6))
line_real, = ax.plot([], [], label='Real part')

# Set plot limits
ax.set_xlim(-5 * np.pi, 5 * np.pi)
ax.set_ylim(-1, 1)
ax.set_title('Morlet Wavelet')
ax.set_xlabel('Time')
ax.set_ylabel('Amplitude')
ax.legend()
ax.grid(True)


def plot_values(arr):
    x_values = [(0 + i*0.1) for i, el in enumerate(arr)]

def plot_values(arr):
    x_values = [(0 + i*0.1) for i,el in enumerate(arr)]
    y_values = arr

    xmin = min(x_values)
    xmax = max(x_values)
    ax.set_xlim(xmin-0.5, xmax+0.5)



def make_it_real(arr):
    out = []
    for el in arr:
        out.append(float(el))
    return out

def update(frame):
    global freq
    global direction
    freq += 0.01
    morlet_wavelet = morlet(M=width, w=1, s=1, complete=True)
    morlet_wavelet = make_it_real(morlet_wavelet)
    line_real.set_data(t, np.real(morlet_wavelet))
    return line_real

def transpose_matrix(m):
    out_untransfomed = list(zip(*m))
    out = []
    for val in out_untransfomed:
        out.append(list(val))
    return out

def matrix_print(m, title="matrix?"):
    print(title)
    row_number = 1
    for row in m:
        print("Row #",row_number,":",end="\t")
        row_number += 1
        print("[",end="\t")
        for val in row:
            print(val, end="\t")
        print("]")
    print("")


exampledata = {1: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
               2: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
               3: [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
               4: [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
               5: [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
               6: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
               7: [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
               8: [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0],
               9: [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
               10:[0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0]
              }


test_matrix = []
for val in exampledata.values():
    test_matrix.append(val)


#checks if 2 sequences match: result gives a dict with 2 vars:
#   - "sensors": the current sequence
#   - "matches": the sensors of the sensors of its match
def match_multiple_seq(sequences1,sequences2, amount_overlapped):
    out = []
    for seq1 in sequences1:
        for seq2 in sequences2:
            if match_single_seq(seq1, seq2, amount_overlapped):
                tmp = dict()
                tmp["sensors"] = seq2
                tmp["matches"] = seq1
                out.append(tmp)
    return out


def match_single_seq(seq1, seq2, amount_overlapped):
    tmp1 = []
    for val in seq1:
        tmp1.append(val[0])
    tmp2 = []
    for val in seq2:
        tmp2.append(val[0])
    return len(set(tmp1) & set(tmp2)) >= amount_overlapped


def find_patterns_from_values_dict(valuedict, threshold, amount_of_sensors=3, amount_overlapped=2):
    data_dict = manoutils.transform_dict_per_timeframe_to_per_sensor(valuedict)
    return find_pattern(data_dict, threshold, amount_of_sensors=3, amount_overlapped=2)


def find_pattern(data_dict,
                 threshold,
                 amount_of_sensors=3,
                 amount_overlapped=2,
                 print_matrix=False,
                 print_consecutives=False,
                 digit_precision=3):
    m = []
    for val in data_dict.values():
        m.append(val)
    m = transpose_matrix(m)

    if print_matrix:
        matrix_print(m, title = "matrix (transposed)")

    consecutives_2D = []
    for row in m:
        last_val_was_positive = False
        consecutives = []
        for i, val in enumerate(row):
            if val >= threshold:
                if last_val_was_positive:
                    consecutives[-1].append((i+1, round(val,digit_precision)))
                else:
                    consecutives.append([(i+1,round(val,digit_precision))])
                last_val_was_positive = True
            else:
                last_val_was_positive = False
        consecutives_2D.append(consecutives)

    for row in consecutives_2D:
        vals_to_delete = []
        for val in row:
            if len(val) < amount_of_sensors:
                vals_to_delete.append(val)
        for val in vals_to_delete:
            row.remove(val)

    if print_consecutives:
        matrix_print(consecutives_2D, "consecutives")

    result = [[]]
    for i in range(len(consecutives_2D))[1:]:
        previous_vals = consecutives_2D[i-1]
        current_vals = consecutives_2D[i]
        result.append(match_multiple_seq(previous_vals, current_vals, amount_overlapped))
    return result


def find_contraction_length(pattern_results, pair, length, rowindex, sequences=[]):
    try:
        for nextpair in pattern_results[rowindex + 1]:
            if nextpair["matches"] == pair["sensors"]:
                sequences.append(pair)
                pattern_results[rowindex].remove(pair)
                return find_contraction_length(pattern_results, nextpair, length + 1, rowindex + 1, sequences=sequences)
    except:
        out = dict()
        out["length"] = length + 1
        out["measure_number"] = rowindex - (length + 1)
        out["sequences"] = sequences
        return out
    out = dict()
    out["length"] = length+1
    out["measure_number"] = rowindex - (length + 1)
    out["sequences"] = sequences
    return out

def find_contractions_from_patterns(pattern_results, contraction_length):
    contractions = []
    for rowindex in range(len(pattern_results)):
        for pair in pattern_results[rowindex]:
            contraction = find_contraction_length(pattern_results, pair, 0, rowindex, sequences=[])#"SEQUENCE=[]" NIET VERWIJDEREN => REFERENCE SEMANTICS
            length = contraction["length"]
            if length >= contraction_length:
                contractions.append(contraction)

    for c in contractions:
        seqs = []
        seqs.append(c["sequences"][0]["matches"])
        for seq in c["sequences"]:
            seqs.append(seq["sensors"])
        c["sequences"] = seqs
    return contractions

"""
def look_up_val_in_data(measure_number, data, sensor):
    return 0
    data = list(data.values())
    return data[measure_number][sensor-1]

def concat_amplitudes_to_contractions(contractions, filedata):
    for c in contractions:
        tmp_seqs = []
        for seq in c["sequences"]:
            tmp_seq = []
            for sensornumber in seq:
                amp = look_up_val_in_data(c["measure_number"], filedata, sensornumber)
                tmp_seq.append((sensornumber,amp))
            tmp_seqs.append(tmp_seq)
        c["sequences"] = tmp_seqs
"""
filedata = manoutils.CSVToDict("functions/Nalox1_18_07_2018.txt")
filedata = manoutils.data_preperation(filedata)
results = find_patterns_from_values_dict(filedata, 10,amount_of_sensors=3,amount_overlapped=2)
iwascrazyonce = find_contractions_from_patterns(results, 10)

print(iwascrazyonce)

