import os
import xlrd
import sys
import json

dataList = []
with open('countries.json', encoding='utf-8') as json_file:
    data = json.load(json_file)
    countries = data['countries']
    vehicletypes = data['vehicletypes']
    speedLimits = data['speedLimits']

def elsoFeladat():
    print("1. feladat")
    speeders = 0
    for i,v in enumerate(dataList):
        felsegjel,rendszam,merohely,jarmutipus,sebesseg,ido = convToStrings(v)
        if merohely == 'A' and jarmutipus == 'm':
            if int(sebesseg) > speedLimits[jarmutipus]:
                speeders += 1
    print(speeders)
    masodikFeladat()

def masodikFeladat():
    print("2. feladat")
    for i,v in enumerate(dataList):
        felsegjel,rendszam,merohely,jarmutipus,sebesseg,ido = convToStrings(v)
        if merohely == 'B' and (jarmutipus == 'sz' or jarmutipus == 'b' or jarmutipus == 't'):
            if int(sebesseg) > speedLimits[jarmutipus]:
                print("Típus: " + converter(jarmutipus) + ", felségjel: " + felsegjel +"(" + str(converter(felsegjel)) + ")" + ", rendszám: " + rendszam + ", túllépés értéke: " + str(int(sebesseg) - speedLimits[jarmutipus]) + "km/h")

def converter(data):
    if data in vehicletypes:
        return vehicletypes[data]
    elif data in countries:
        return countries[data]
    else:
        return "ismeretlen"
     

def convToList(fileType, Thefile):
    if fileType == 1:
        for line in Thefile:
            dataList.append(line)
    elif fileType == 2:
        for x in range(Thefile.nrows):
            dataList.append(Thefile.cell_value(x,0))
    elsoFeladat()

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

