# Automatically-Simulations-CORSIKA
Program to do automatically simulation in CORSIKA


# IMPORTANT
- Make sure you have installed Python 3~, root cern and c++ on your computer

- Before running this code, you must create a folder called "Simulations" in the root folder of the CORSIKA program. The information of each group of simulations will be stored in this folder.

- All files should be copied to the CORSIKA "run" folder

- To run the program run the following command from the Linux terminal:

    source ejecutar.sh




------- Descripción de las variables, para la información consulta el programa Automatic_runners.py
 
- #######################HEADER########################
- ###----> FIRST PART OF THE PROGRAM SIMULATES USING CORSIKA FOR A RANGE OF ENERGIES.
- ###----> VARIABLES DEFINITIONS 
- ###----> motherFolder => name of the folder in which the output information will be saved
- ###----> nshow => number of showers per simulation
- ###----> ERANGE => range of energies (array type)
- ###----> PRMPAR => type of particles to simulation (array type)
- ###----> places => the file contains the information about the places to be simulated.

