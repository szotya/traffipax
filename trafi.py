import os, xlrd, sys, json, re, datetime

dataList = []
devicePlaces = {}
ANeighbors = ['B']
BNeighbors = ['A', 'C']
CNeighbors = ['B']

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
                print("Típus: " + converter(jarmutipus) + ", felségjel: " + felsegjel + converter(felsegjel) + ", rendszám: " + rendszam + ", túllépés értéke: " + str(int(sebesseg) - speedLimits[jarmutipus]) + "km/h")
    harmadikFeladat()

def harmadikFeladat():
    print("3. feladat")
    maxSpeed = 0
    maxSpeeders = []
    for i,v in enumerate(dataList):
        felsegjel,rendszam,merohely,jarmutipus,sebesseg,ido = convToStrings(v)
        if merohely == 'C' and int(sebesseg) > maxSpeed:
            maxSpeed = int(sebesseg)
            maxSpeeders.clear()
            maxSpeeders.append(i)
        elif merohely == 'C' and int(sebesseg) == maxSpeed:
            maxSpeeders.append(i)
    for v in maxSpeeders:
        felsegjel,rendszam,merohely,jarmutipus,sebesseg,ido = convToStrings(dataList[v])
        if int(sebesseg) > speedLimits[jarmutipus]: 
            tullepes = "túllépte"
        else:
            tullepes = "nem_lépte_túl"
        print(sebesseg + "km/h", tullepes, converter(jarmutipus), felsegjel + converter(felsegjel) ,rendszam,ido)
    negyedikFeladat()

def negyedikFeladat():
    print("4. feladat")
    correct_format = re.compile('^[a-zA-Z]{3}-[0-9]{3}$')
    counter = 0
    crossedVeh = []
    for i,v in enumerate(dataList):
        felsegjel,rendszam,merohely,jarmutipus,sebesseg,ido = convToStrings(v)
        if correct_format.match(rendszam) is not None:
            if rendszam not in crossedVeh:
                counter += 1
                crossedVeh.append(rendszam)
    print(counter)
    otodikFeladat()

def otodikFeladat():
    print("5. feladat")
    for i,v in enumerate(dataList):
        felsegjel,rendszam,merohely,jarmutipus,sebesseg,ido = convToStrings(v)
        if merohely == 'C' and is_between(ido,('09:00:01', '13:00:01')):
            if int(sebesseg) <= speedLimits[jarmutipus] and int(sebesseg) > 110:
                print(felsegjel+converter(felsegjel),rendszam,sebesseg+"km/h",ido)
    hatodikFeladat()

def hatodikFeladat():
    print("6. feladat")
    crossedVehicles = []
    multipleCrosses = []
    multipleCrossed_id = []
    for i,v in enumerate(dataList):
        felsegjel,rendszam,merohely,jarmutipus,sebesseg,ido = convToStrings(v)
        if rendszam in crossedVehicles:
            multipleCrosses.append(rendszam)
        else:
            crossedVehicles.append(rendszam)
    for i,v in enumerate(dataList):
        felsegjel,rendszam,merohely,jarmutipus,sebesseg,ido = convToStrings(v)
        if rendszam in multipleCrosses:
            multipleCrossed_id.append(i)
    iter_multipleCrossed_id = iter(multipleCrossed_id)
    next(iter_multipleCrossed_id)
    for i,v in enumerate(iter_multipleCrossed_id):
        felsegjel1,rendszam1,merohely1,jarmutipus1,sebesseg1,ido1 = convToStrings(dataList[int(v-1)])
        felsegjel2,rendszam2,merohely2,jarmutipus2,sebesseg2,ido2 = convToStrings(dataList[v])
        if merohely1 in merConv(merohely2) and rendszam1 == rendszam2:
            elapsedTime = datetime.datetime.strptime(ido2,'%H:%M:%S') - datetime.datetime.strptime(ido1,'%H:%M:%S')
            hours = elapsedTime.total_seconds()/3600
            totalDistance = int(devicePlaces[merohely2]) - int(devicePlaces[merohely1])
            avgSpeed = totalDistance/hours
            if avgSpeed > speedLimits[jarmutipus1]:
                print(felsegjel + converter(felsegjel1),rendszam1, merohely1 + " -> " + merohely2, str(avgSpeed) + "km/h")
    

def is_between(time, time_range):
    if time_range[1] < time_range[0]:
        return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]

def merConv(data):
    if data == 'A':
        return ANeighbors
    elif data == 'B':
        return BNeighbors
    elif data == 'C':
        return CNeighbors

def converter(data):
    if data in vehicletypes:
        return vehicletypes[data]
    elif data in countries:
        return "(" + countries[data] + ")"
    else:
        return "ismeretlen" 

def convToList(fileType, Thefile):
    #.txt
    if fileType == 1:
        places = Thefile.readline()
        strings = convToStrings(places)
        letter = ''
        for index,place in enumerate(strings):
            if index == 0:
                 letter = 'A' 
            elif index == 1:
                 letter = 'B'
            elif index == 2:
                letter = 'C'
            devicePlaces[letter] = place
        for line in Thefile:
            dataList.append(line.strip())
    #.xlsx -->todo: excel első sorból kiolvasás még nem jó
    elif fileType == 2:
        places = Thefile.cell_value(0,0)
        strings = convToStrings(places)
        for place in strings:
            devicePlaces.append(place)
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
