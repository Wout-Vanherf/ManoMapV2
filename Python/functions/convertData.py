def convertData(data):
    #check if first entry is wrong format (Name=...)
    try:
        substr = data[0][0][:len('Name=')]
    except:
        substr = ''
    if substr == 'Name=':
        #delete first 7 lines
        data = data[7:]
        #divide first entry by 10 to get 1/10th of second
        for line in data:
            line[0] = line[0]/10
        return data
    else:
        return data


#test
if __name__ == '__main__':
    data = [
    ["Name=t"],
    [2],
    [3],
    [4],
    [5],
    [6],
    [7],
    [8, 'random'],
    ]

    new_data = convertData(data)
    print(new_data)