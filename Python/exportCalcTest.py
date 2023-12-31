import manoutils
import xml.etree.ElementTree as ET

contractionsList = [{'length': 54, 'measure_number': 9099, 'sequences': [[(32, 263.543), (33, 125.697), (34, 27.113)], [(32, 247.99), (33, 128.945), (34, 68.404)], [(32, 226.239), (33, 130.863), (34, 96.299)], [(32, 223.044), (33, 133.117), (34, 99.256)], [(32, 211.382), (33, 135.058), (34, 107.261)], [(32, 209.365), (33, 141.237), (34, 120.161)], [(32, 208.882), (33, 142.194), (34, 126.222)], [(32, 193.792), (33, 125.055), (34, 140.373)], [(32, 171.807), (33, 103.616), (34, 149.29)], [(32, 166.442), (33, 97.084), (34, 152.303)], [(32, 158.472), (33, 96.422), (34, 154.142)], [(32, 142.973), (33, 90.126), (34, 152.951)], [(32, 131.725), (33, 81.813), (34, 139.095)], [(32, 120.856), (33, 76.059), (34, 135.613)], [(32, 103.449), (33, 73.902), (34, 136.24)], [(32, 105.342), (33, 74.583), (34, 138.209)], [(32, 114.587), (33, 75.707), (34, 139.982)], [(32, 103.352), (33, 73.713), (34, 144.504)], [(32, 91.117), (33, 69.212), (34, 145.51)], [(32, 96.797), (33, 70.703), (34, 139.676)], [(32, 102.646), (33, 72.158), (34, 137.998)], [(32, 94.496), (33, 69.88), (34, 135.617)], [(32, 85.397), (33, 62.143), (34, 133.966)], [(32, 87.208), (33, 63.672), (34, 135.006)], [(32, 89.788), (33, 66.379), (34, 135.023)], [(32, 85.674), (33, 65.956), (34, 134.469)], [(32, 76.982), (33, 55.359), (34, 136.366)], [(32, 79.909), (33, 56.552), (34, 138.851)], [(32, 91.616), (33, 69.818), (34, 142.246)], [(32, 89.107), (33, 71.701), (34, 149.586)], [(32, 79.15), (33, 62.547), (34, 148.743)], [(32, 82.216), (33, 63.145), (34, 152.754)], [(32, 93.409), (33, 75.6), (34, 153.141)], [(32, 89.77), (33, 76.852), (34, 157.099)], [(32, 73.707), (33, 64.918), (34, 156.81)], [(32, 73.991), (33, 62.715), (34, 156.914)], [(32, 81.835), (33, 70.678), (34, 156.743)], [(32, 81.306), (33, 75.305), (34, 154.189)], [(32, 72.631), (33, 66.332), (34, 155.048)], [(32, 72.064), (33, 64.083), (34, 149.577)], [(32, 66.233), (33, 58.207), (34, 140.232)], [(32, 53.449), (33, 45.907), (34, 130.769)], [(32, 45.63), (33, 40.057), (34, 121.332)], [(32, 45.787), (33, 59.184), (34, 121.867)], [(32, 41.834), (33, 58.914), (34, 120.103)], [(32, 40.046), (33, 57.371), (34, 119.994)], [(32, 37.046), (33, 54.527), (34, 120.68)], [(32, 35.554), (33, 54.077), (34, 118.486)], [(32, 34.911), (33, 46.54), (34, 116.286)], [(32, 32.269), (33, 49.826), (34, 116.006)], [(32, 30.456), (33, 61.08), (34, 115.789)], [(32, 29.308), (33, 54.798), (34, 115.806)], [(32, 27.027), (33, 51.854), (34, 117.377)], [(32, 25.002), (33, 58.58), (34, 119.04)]]}, 
                    {'length': 6, 'measure_number': 9222, 'sequences': [[(10, 278.676), (11, 69.757), (12, 108.312)], [(10, 124.69), (11, 70.021), (12, 211.53)], [(11, 74.565), (12, 260.881), (13, 50.505)], [(11, 67.791), (12, 212.474), (13, 98.39), (14, 64.828)], [(11, 44.175), (12, 144.407), (13, 116.299), (14, 114.49)], [(11, 22.069), (12, 75.714), (13, 102.554), (14, 125.523)]]}]

"""header = [
    ['Time', 'Ant/Retr', 'Amplitude', 'Velocity', 'startSensor', 'endSensor', 'lengthContraction']
    ]"""
distance = 3
contractions = []
first = 1
last = 1
for line in contractionsList:
    max_y_values = []
    contractionsDict = dict()
    for entry in line['sequences']:
        max_y_values.append(max(entry, key=lambda x: x[1])[1])
        for point in entry:    
            try:
                if contractionsDict[point[0]] < point[1]:
                    contractionsDict[point[0]] = point[1]
            except:
                contractionsDict[point[0]] = point[1]
    maxAmp = max(max_y_values)
    gran = manoutils.get_granularity_factor()
    time = gran * len(line['sequences'])
    velocity = (line['sequences'][-1][-1][0] - line['sequences'][0][0][0])*distance/time*10
    if velocity > 0:
        direction = "Ant"
    else:
        direction = "Retr"

    contract = [manoutils.convertTimeToText(manoutils.get_granularity_factor() * line['measure_number']), direction, maxAmp, str(velocity) + 'cm/s', line['sequences'][0][0][0], line['sequences'][-1][-1][0], line['length']]
    count = first
    while count -1 < last:
        try:
            contract.append(contractionsDict[count])
        except:
            contract.append(None)
        count += 1

    contractions.append(contract)
#print(contractions)


contractions = []
contractionsDict = dict()
for line in contractionsList:
        #calculate max amplitude
    max_y_values = []
    contractionsDict = dict()
    print(len(max_y_values))
    for entry in line['sequences']:
        max_y_values.append(max(entry, key=lambda x: x[1])[1])
        #make a dict with amp per sensor
        for point in entry:    
            try:
                if contractionsDict[point[0]] < point[1]:
                    contractionsDict[point[0]] = point[1]
            except:
                contractionsDict[point[0]] = point[1]
    maxAmp = max(max_y_values)
    print(contractionsDict)

"""<sequences>
        <range  channel="6" maxSample="145508" maxValue="17.38321"/>
        <range channel="7" maxSample="145522" maxValue="25.29626"/>
        <range channel="8"maxSample="145513" maxValue="24.287949"/>
    </sequence>"""
"""
max_values = []

# for each contraction, check highest value per sensor and what time
for line in contractionsList:
    max_values_per_line = {}
    count = line['measure_number']
    for sublist in line['sequences']:
        for x, y in sublist:
            if x in max_values_per_line:
                if y > max_values_per_line[x][0]:
                    max_values_per_line[x] = (y, count)
            else:
                max_values_per_line[x] = (y, count)
        count += 1
    max_values.append(max_values_per_line)

print(max_values)
"""


"""
root = ET.Element("sequences")

# Create the first sequence element
count = 0
for entry in contractions:
    sequence1 = ET.SubElement(root, "sequence", dir="", vel=velocity, startSample="145508", endSample="145522", startChannel="6", endChannel="8")

        # Create range elements for the first sequence
    for channel in range(6, 9):
        range_elem = ET.SubElement(sequence1, "range", startSample="145508", endSample="145522", channel=str(channel), minSample="145522", maxSample="145508")
        range_elem.set("minValue", str(9.728966))
        range_elem.set("maxValue", str(17.38321))

    # Create an ElementTree
tree = ET.ElementTree(root)

    # Manually add the XML declaration with the standalone attribute
xml_declaration = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
with open("output.xml", "wb") as file:
    file.write(xml_declaration.encode('utf-8'))
    tree.write(file, encoding="utf-8")
    
    count += 1

#print(contractionsDict)
"""