import pandas as pd
import numpy as np
import os 
import subprocess as sps
import re
from io import open
import random
import fnmatch
from natsort import natsorted

#######################HEADER########################
###----> FIRST PART OF THE PROGRAM SIMULATES USING CORSIKA FOR A RANGE OF ENERGIES.
###----> VARIABLES DEFINITIONS 
###----> mainFolder => name of the folder in which the output information will be saved
###----> nshow => number of showers per simulation
###----> ERANGE => primary energies (array type)
###----> PRMPAR => type of particles to simulation (array type)
###----> places => the file contains the information about the places to be simulated.

"""------------------------HEADS---------------------------"""

print("Hello, this program allows you simulate in CORSIKA in an automated way.")
print("\n -.........................................................................- \n")

mainFolder = str(input("Insert a name for the main folder: "))

nshow = int(input("Insert the number of shower per runner: ")) 

places = pd.read_csv("Places_data.txt", header = 0, delim_whitespace=True)

PRMPAR = np.array([1, 14, 402, 1407, 5626])

ERANGE = np.concatenate((np.arange(0.1, 10, 0.3),np.power(10, np.arange(1, 5+0.025, 0.025)))) 

def index(places): ###FUNCION SOLO PARA LOS INDICES
    index_city = np.array(places.index)
    for i in index_city:
        os.system("mkdir ../Simulations/{}/{}".format(mainFolder,i))

"""-----------XX-----------HEADS------------XX-------------"""

"""------------------------MAIN CODE-----------------------"""

os.system("mkdir ../Simulations/{}".format(mainFolder))
index(places)

######### OPENNING AND READING OF ALL-INPUTS.TXT FILE ##########

with open('all-inputs.txt', 'r') as texto1:
    Input = texto1.read()

with open("readpartExample.cc", "r") as Text1:
    Reader = Text1.read()

#XXXXXXXX OPENNING AND READING OF ALL-INPUTS.TXT FILE XXXXXXXXXX

######### MAIN PART #########

def partIndetify(id):
    if id == 1:
        return "Gamma"
    if id == 14:
        return "Proton"
    if id == 402:
        return "Helium"
    if id == 1407:
        return "Nitrogen"
    if id == 5626:
        return "Iron"
    return id

def mainFunction(places):
    counter = 1
    seedHad = 1
    seedElec = 2

    for i,r,mx,mz in zip(places["Height"], np.array(places.index), places["MagnetX"], places["MagnetZ"]):
        for j in PRMPAR:
            os.system('mkdir ../Simulations/{}/{}/{}'.format(mainFolder, r, partIndetify(j)))
            os.system('mkdir ../Simulations/{}/{}/{}/Binaries'.format(mainFolder, r, partIndetify(j)))
            for l in zip(ERANGE):
                all_inputs = open('all-inputs{}'.format(counter), 'w')
                all_inputs.write(Input.format(counter, nshow, j, l, l, seedHad, seedElec, i, mx, mz))
                all_inputs.close()
                os.system("./corsika77410Linux_QGSII_urqmd_thin <all-inputs{}> output{}.txt".format(counter,counter))
                
                binDatFile = "DAT{}".format(str(counter).zfill(6))
                corsikaReader = open('readpartExample{}.cc'.format(counter), 'w')
                corsikaReader.write(Reader.replace(":v", binDatFile))
                corsikaReader.close()
                sps.run(["make"], shell = True)

                os.system("./readpartExample{} {} >> Data{}.txt".format(counter, binDatFile, counter))
                os.system("rm readpartExample{} readpartExample{}.cc".format(counter,counter))
                os.system("mv {} {}.long ../Simulations/{}/{}/{}/Binaries".format(binDatFile, binDatFile, mainFolder, r, partIndetify(j)))
                os.system("mv Data{}.txt ../Simulations/{}/{}/{}".format(counter, mainFolder, r, partIndetify(j)))    

                os.system("rm all-inputs{}".format(counter))
                os.system("mv output{}.txt ../Simulations/{}/{}/{}/Binaries".format(counter, mainFolder, r, partIndetify(j)))
                counter += 1
                seedHad += 1
                seedElec += 2
                os.system("clear")
            del(seedHad, seedElec)

mainFunction(places)

#XXXXXXXX MAIN PART XXXXXXXXX



############### THE FOLLOWING FUNCTION IS EXECUTED DIRECTLY IN THE FOLDER WHERE THE CORSIKA BINARIES ARE LOCATED############
###THIS PROGRAM WAS CREATED TO BREAK A CODE THE BINARY FILES THAT CORSIKA GIVE US AFTER THE SIMULATIONS


seq = "DAT*"

def filesFilter(seq):
    allFiles = os.listdir("./")
    dFilesSelect = np.array([])
    for i in allFiles:
        if fnmatch.fnmatch(i, seq):
            dFilesSelect = np.append(dFilesSelect, i)
    return np.array(natsorted(dFilesSelect, key = lambda y: y.lower()))

def readOnly(seq):
    filesName = filesFilter(seq)
    with open("readpartExample.cc", "r") as Text1:
        Reader = Text1.read()
    for i in filesName:
        pureID =  re.findall(r'\d+', i)[0].lstrip("0")
        corsikaReader = open('readpartExample{}.cc'.format(pureID), 'w')
        corsikaReader.write(Reader.replace(":v", i))
        corsikaReader.close()
        sps.run(["make"], shell = True)

        os.system('./readpartExample{} {} >> Data{}.txt'.format(pureID, i, pureID))
        os.system('rm readpartExample{} readpartExample{}.cc'.format(pureID, pureID))


#readOnly(seq)
    