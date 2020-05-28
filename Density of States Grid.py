# Density of States (definitly electronic, maybe phonons later)

import matplotlib.pyplot as plt
import DensityOfStatesHeader as dos
import re

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.tight_layout = True

SAVE_LOC = "C://Users//baron//Desktop//DOSgraph.png"

directories = ["C://Users//baron//Desktop//Real DOSCAR Res//minEnergy//pure//dos//DOSCAR",
               "C://Users//baron//Desktop//Real DOSCAR Res//minEnergy//sv//dos//DOSCAR",
               "C://Users//baron//Desktop//Real DOSCAR Res//minEnergy//dv//dos//DOSCAR",
               "C://Users//baron//Desktop//Real DOSCAR Res//minEnergy//dvSkew//dos//DOSCAR",
               "C://Users//baron//Desktop//Real DOSCAR Res//minEnergy//555777//dos//DOSCAR",
               "C://Users//baron//Desktop//Real DOSCAR Res//minEnergy//swsSkew//dos//DOSCAR",
               "C://Users//baron//Desktop//Real DOSCAR Res//minEnergy//sws//dos//DOSCAR",
               "C://Users//baron//Desktop//Real DOSCAR Res//xStrain//pure//dos//DOSCAR",
               "C://Users//baron//Desktop//Real DOSCAR Res//xStrain//sv//dos//DOSCAR",
               "C://Users//baron//Desktop//Real DOSCAR Res//xStrain//dv//dos//DOSCAR",
               "C://Users//baron//Desktop//Real DOSCAR Res//xStrain//dvSkew//dos//DOSCAR",
               "C://Users//baron//Desktop//Real DOSCAR Res//xStrain//555777//dos//DOSCAR",
               "C://Users//baron//Desktop//Real DOSCAR Res//xStrain//swsSkew//dos//DOSCAR",
               "C://Users//baron//Desktop//Real DOSCAR Res//xStrain//sws//dos//DOSCAR",
               "C://Users//baron//Desktop//Real DOSCAR Res//yStrain//pure//dos//DOSCAR",
               "C://Users//baron//Desktop//Real DOSCAR Res//yStrain//sv//dos//DOSCAR",
               "C://Users//baron//Desktop//Real DOSCAR Res//yStrain//dv//dos//DOSCAR",
               "C://Users//baron//Desktop//Real DOSCAR Res//yStrain//dvSkew//dos//DOSCAR",
               "C://Users//baron//Desktop//Real DOSCAR Res//yStrain//555777//dos//DOSCAR",
               "C://Users//baron//Desktop//Real DOSCAR Res//yStrain//swsSkew//dos//DOSCAR",
               "C://Users//baron//Desktop//Real DOSCAR Res//yStrain//sws//dos//DOSCAR"               
               ]

#MAIN------------------------------------------------------------------------    
allFiles = []

##calculate difference between true num electrons and approx number electrons
#for d in directories:
#    spinPol = False
#    if(re.search("sv", d)):
#        spinPol = True
#    head = dos.ReadDoscarHead(d)
#    allDos = dos.GetAtomDosInfo(d, 0, spin = spinPol)
#    i = 0
#
#    if(spinPol):
#        while(True):
#            if(allDos["energy"][i] > allDos["eFermi"]):
#                print((4*head["nAtoms"]) - (allDos["intDos(up)"][i-1] + allDos["intDos(dn)"][i-1]))
#                break
#            i = i + 1
#    else:
#        while(True):
#            if(allDos["energy"][i] > allDos["eFermi"]):
#                print((4*head["nAtoms"]) - allDos["intDos"][i-1])
#                break
#            i = i + 1



##for orbital decomposed
#for d in directories:
#    spinPol = False
#    head = dos.ReadDoscarHead(d)
#    fullDosData = dos.GetEnergyInfo(d, 0) ##0th atom corresponds to the full system
#    nedos = fullDosData["NEDOS"]    
#    nAtoms = head["nAtoms"]
#    if(re.search("sv", d)):
#        spinPol = True
#    allDos = dos.AtomGroup(d, [1, nAtoms], nedos, spin = spinPol, atomType="C")
#    allFiles.append(allDos)
#    print(str(d), " completed.\n")
#dos.DOSGridGraphAtom("a", SAVE_LOC, ".pdf", allFiles, suppressD = True)


#for full DOS
for d in directories:
    spinPol = False
    if(re.search("sv", d)):
        spinPol = True
    allDos = dos.GetAtomDosInfo(d, 0, spin = spinPol)
    allFiles.append(allDos)
dos.DOSGridGraphFull("a", SAVE_LOC, ".pdf", allFiles)








            






    
