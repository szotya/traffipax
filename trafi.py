import os
import xlrd
import sys

dataList = []

def convToList(fileType, Thefile):
    if fileType == 1:
        for line in Thefile:
            dataList.append(line)
    elif fileType == 2:
        for x in range(Thefile.nrows):
            dataList.append(Thefile.cell_value(x,0))
    print(dataList)


def choose():
    print("Kérem ajda meg a fájl elérési útvonalát: ")
    filePath = input()
    if os.path.exists(filePath):
        if filePath.endswith('.txt'):
            theFile = open(filePath, 'r')
            convToList(1,theFile)
        elif filePath.endswith('.xlsx'):
            inpWorkbook = xlrd.open_workbook(filePath)
            inWorksheet = inpWorkbook.sheet_by_index(0)
            convToList(2, inWorksheet)
        else:
            print('Hibás fájlformátum(.txt/.xlsx)')
    else:
        print('Hibás elérési útvonal!')
        choose()

choose()

        