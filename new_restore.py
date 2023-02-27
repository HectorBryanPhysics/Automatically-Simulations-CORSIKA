import pandas as pd
import numpy as np
from io import open
import os

#######################HEADER########################
###----> FIRST PART OF THE PROGRAM SIMULATES USING CORSIKA FOR A RANGE OF ENERGIES.
###----> VARIABLES DEFINITIONS 
###----> motherFolder => name of the folder in which the output information will be saved
###----> nshow => number of showers per simulation
###----> ERANGE => range of energies (array type)
###----> PRMPAR => type of particles to simulation (array type)
###----> places => the file contains the information about the places to be simulated.

"""------------------------HEADS---------------------------"""

motherFolder = "Run6" 

def index(places): ###FUNCION SOLO PARA LOS INDICES
    index_city = np.array(places.index)
    for i in index_city:
        os.system("mkdir ../Simulations/{}/{}".format(motherFolder,i))

places = pd.read_csv("Places_data.txt", header = 0, delim_whitespace=True)

PRMPAR = Particles_array = [1, 14, 402, 1407, 5626]

ERANGE = np.concatenate((np.arange(0.1, 10, 0.3),np.power(10, np.arange(1, 5+0.025, 0.025)))) 

"""-----------XX-----------HEADS------------XX-------------"""

"""------------------------MAIN CODE-----------------------"""

if __name__ == '__main__':
    print("\nHello, this program allows you simulate in CORSIKA in an automated way.\n")
    print("\n -.........................................................................- \n")
    os.system("mkdir ../Simulations/{}".format(motherFolder))
    index(places)
    nshow = int(input("Insert the number of shower per runner: ")) 

    '--------------------------- OPENNING AND READING OF ALL-INPUTS.TXT FILE--------------------------'

    with open('all-inputs.txt', 'r') as texto1:
        Input = texto1.read()

    '--------------X------------ OPENNING AND READING OF ALL-INPUTS FILE-------------X------------'

    '-------------------------CREATING GENERATORS OF EACH SIMULATION-------------------------'

    def SEED_HAD(): ## GENERATOR TO SEED FOR THE HADRONIC PART
        SEEDH = 1
        counterh = 1
        while counterh <= places["Height"].size*PRMPAR.size*ERANGE.size:
            yield (SEEDH)
            SEEDH += 2
            counterh += 1

    SEED_HAD = SEED_HAD()

    def SEED_EGS4(): ## GENERATOR TO SEED FOR THE ELECTROMAGNETIC PART
        SEEDE = 1
        countere = 1
        while countere <= places["Height"].size*PRMPAR.size*ERANGE.size:
            yield (SEEDE*2)
            SEEDE += 1
            countere+=1

    SEED_EGS4=SEED_EGS4()

    '-------------X------------CREATING GENERATORS OF EACH SIMULATION-------------X------------'

    '----------------------MAIN PART----------------------'

    counter = 1 

    for i,r,mx,mz in zip(places["Height"], np.array(places.index), places["MagnetX"], places["MagnetZ"]):
        for j in PRMPAR:
            os.system('mkdir ../Simulations/{}/{}/{}'.format(motherFolder, r, j))
            os.system('mkdir ../Simulations/{}/{}/{}/Binaries'.format(motherFolder, r, j))
            for l,m,n in zip(ERANGE, SEED_HAD, SEED_EGS4):
                all_inputs = open('all-inputs{}'.format(counter), 'w')
                all_inputs.write(Input.format(counter, nshow, j, l, l, m, n, i, mx, mz))
                all_inputs.close()
                os.system("./corsika77410Linux_QGSII_urqmd_thin <all-inputs{}> output{}.txt".format(counter,counter))
                os.system("rm all-inputs{}".format(counter))
                os.system("mv output{}.txt ../Simulations/{}/{}/{}/Binaries".format(counter, motherFolder, r, j))
                counter += 1

    '---------------------CORSIKA READER OF BIN FILES----------------------------'

    with open('readpartExample.cc', 'r') as Text2:
        Reader = Text2.read()

    for i in np.arange(1,PRMPAR.size*ERANGE.size*places["Height"].size+1):
        Corsika_reader = open('readpartExample{}.cc'.format(i), 'w')
        Corsika_reader.write(Reader.replace(":v", "DAT{}".format(str(i).zfill(6))))

    '----------X-----------CORSIKA READER OF BIN FILES--------------X------------'

"""------------------------MAIN CODE-----------------------"""



