import os
import xlrd
import sys

dataList = []
speedLimits = {
    'sz': 130,
    'm': 130,
    'b': 100,
    't': 80,
    'mk': 1000 # "nincs korlát"
}
def elsoFeladat():
    speeders = 0
    for i,v in enumerate(dataList):
        felsegjel,rendszam,merohely,jarmutipus,sebesseg,ido = convToStrings(v)
        if merohely == 'A' and jarmutipus == 'm':
            if int(sebesseg) > speedLimits[jarmutipus]:
                speeders += 1
    print(speeders)
    masodikFeladat()

def masodikFeladat():
    print("aa")
    
def convToList(fileType, Thefile):
    if fileType == 1:
        for line in Thefile:
            dataList.append(line)
    elif fileType == 2:
        for x in range(Thefile.nrows):
            dataList.append(Thefile.cell_value(x,0))
    elsoFeladat()
    print(dataList)           

def convToStrings(data):
    strings = data.split(",", -1)
    return strings

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

