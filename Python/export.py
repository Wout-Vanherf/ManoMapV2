import openpyxl
from openpyxl.styles import PatternFill

# Sample header (you can replace this with your own header)
header = [
    ['Time', 'Ant/Retr', 'Amplitude', 'Velocity', 'startSensor', 'endSensor', 'lengthContraction']
]

def createExcelWorkBook(name,startAscending,startTransverse,startDescending,startSigmoid,startRectum,endRectum, data):
# Create a new Excel workbook and add a worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Data"
    headerSize = len(header[0]) 
#add regions
    count = 0
    while startAscending + count < startTransverse:
        header[0].append('Ascending' + str(startAscending + count))
        count += 1
    count = 0
    while startTransverse + count < startDescending:
        header[0].append('Transverse' + str(startTransverse + count))
        count += 1
    count = 0
    while startDescending + count < startSigmoid:
        header[0].append('Descending' + str(startDescending + count))
        count += 1
    count = 0
    while startSigmoid + count < startRectum:
        header[0].append('Sigmoid' + str(startSigmoid + count))
        count += 1
    count = 0
    while not startRectum + count >endRectum:
        header[0].append('Rectum' + str(startRectum + count))
        count += 1
#try to append data to the header
    try:
        for line in data:
            header.append(line)
    except:
        print("error in datalijn toevoegen")    
# Write the header to the worksheet
    for row in header:
        worksheet.append(row)
#colour regions
#length of regions
    lenAsc = startTransverse - startAscending
    lenTrans = startDescending - startTransverse
    lenDesc = startSigmoid - startDescending
    lenSig = startRectum - startSigmoid
    lenRect = endRectum - startRectum + 1
#decide where regions stop   
    stopAsc = headerSize +lenAsc
    stopTrans = stopAsc+lenTrans
    stopDesc = stopTrans+lenDesc
    stopSig = stopDesc+lenSig
    stopRect = stopSig+lenRect

#color the regions to distinguish them
    fill = PatternFill(start_color="00FF00", end_color="00FF00", fill_type="solid")
    for row in worksheet.iter_rows(min_row=1, max_row=1, min_col=8, max_col=stopAsc):
        for cell in row:
            cell.fill = fill

    fill = PatternFill(start_color="000099", end_color="000099", fill_type="solid")
    for row in worksheet.iter_rows(min_row=1, max_row=1, min_col=1+stopAsc, max_col=stopTrans):
        for cell in row:
            cell.fill = fill

    fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")
    for row in worksheet.iter_rows(min_row=1, max_row=1, min_col=1+stopTrans, max_col=stopDesc):
        for cell in row:
            cell.fill = fill
    
    fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
    for row in worksheet.iter_rows(min_row=1, max_row=1, min_col=1+stopDesc, max_col=stopSig):
        for cell in row:
            cell.fill = fill

    fill = PatternFill(start_color="00FFFF", end_color="00FFFF", fill_type="solid")
    for row in worksheet.iter_rows(min_row=1, max_row=1, min_col=1+stopSig, max_col=stopRect):
        for cell in row:
            cell.fill = fill


# Specify the XLSX file name
    xlsx_file = name + ".xlsx"
# Save the workbook to the specified file
    workbook.save(xlsx_file)

if __name__ == '__main__':
    #elke regio is 1 lang => nooit dubbel in xlsx
    createexcelWorkBook('test',1,5,6,7,8,8, [[1,"A",10,1,1,5,4,10,10,10,10,0,0,0,0]])