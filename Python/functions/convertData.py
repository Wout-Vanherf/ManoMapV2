def convertData(data):
    #check of eerste entry van het fout format is (Name=...)
    eerste_paar_letters = data[0][0][:len('Name=')]
    if eerste_paar_letters == 'Name=':
        #delete de eerste 7 lines
        return data[7:]
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
    [8],
    ]

    new_data = convertData(data)
    print(new_data)