from io import open
import os
import numpy as np
from Automatic_runners import *

contador = 1

for r in np.array(places.index):
    for j in PRMPAR:
        for l in ERANGE:
            os.system("./readpartExample{} DAT{} >> Data{}.txt".format(contador, str(contador).zfill(6), contador))
            os.system("rm readpartExample{} readpartExample{}.cc".format(contador,contador))
            os.system("mv DAT{} DAT{}.long ../Simulations/{}/{}/{}/Binaries".format(str(contador).zfill(6), str(contador).zfill(6), motherFolder, r, j))
            os.system("mv Data{}.txt ../Simulations/{}/{}/{}".format(contador, motherFolder, r, j))    
            contador += 1
            
            