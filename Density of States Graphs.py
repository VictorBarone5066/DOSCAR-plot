# Density of States (definitly electronic, maybe phonons later)

import matplotlib.pyplot as plt
import DensityOfStatesHeader as dos

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.tight_layout = True

DOSCAR_LOC = "C://Users//baron//Desktop//Real DOSCAR Res//minEnergy//pure//dos//DOSCAR"
POSCAR_LOC = "C://Users//baron//Desktop//POSCAR"
SAVE_LOC = "C://Users//baron//Desktop//"


#MAIN------------------------------------------------------------------------    
'''
ATOMS OF INTEREST (compare to pure graphene):
SV(eMin):   **64, 8, 11**, 26, 29, 61, 67, 44, 49, 25, 28, 63 (stars are the "triangle" of the vac)
DV(eMin):   26, 29, 61, 66, 44, 49, 8, 11 (all atoms immediatly around the vac) 
'''


#LDOS Plots
fullDosData = dos.GetEnergyInfo(DOSCAR_LOC, 0)
nedos = fullDosData["NEDOS"]
ldos = dos.AtomGroup(DOSCAR_LOC, [0], nedos, atomVals = [26, 29, 61, 66, 44, 49, 8, 11], atomType = 'C', spin = False)
ldos.PlotThisAtom(suppressD = True)

plt.xlabel(r"$E-E_\mathrm{F}$ (eV)")
plt.ylabel("DOS (states / eV / number of atoms)")

#fullDosData = dos.GetEnergyInfo(DOSCAR_LOC, 0) ##0th atom corresponds to the full system
#fullDosValues = dos.GetAtomDosInfo(DOSCAR_LOC, 0, spin=True)

#eFermi = fullDosData["eFermi"]
#nedos = fullDosData["NEDOS"]
#energies = fullDosValues["energy"]
#fullDos = fullDosValues["dos"]

##For AgBiI
#ranges = dos.ScanPoscar(POSCAR_LOC)
#for r in ranges:
#    mi = dos.AtomGroup(DOSCAR_LOC, r[1], nedos, atomType = r[0])
#    mi.PlotThisAtom()

##For Graphene w/o POSCAR
#nAtoms = head["nAtoms"]
#allDos = dos.AtomGroup(DOSCAR_LOC, [1, nAtoms], nedos, spin = False, atomType = 'C')
#allDos.PlotThisAtom(suppressD = True)

#Differences between two files
#fileLocs = ["C://Users//baron//Desktop//Real DOSCAR Res//minEnergy//sv//dos//DOSCAR",
#            "C://Users//baron//Desktop//Real DOSCAR Res//xStrain//sv//dos//DOSCAR",
#            "C://Users//baron//Desktop//Real DOSCAR Res//yStrain//sv//dos//DOSCAR"]
#d1, d2, d3 = dos.GetAtomDosInfo(fileLocs[0], 0, spin = True), dos.GetAtomDosInfo(fileLocs[1], 0, spin = True), dos.GetAtomDosInfo(fileLocs[2], 0, spin = True)  
#dosDiff = dos.Difference(d1["dos(up)"], d1["dos(dn)"])
#eScaled = [e - d1["eFermi"] for e in d1["energy"]]
#plt.plot(eScaled, dosDiff, 'k')
#
#plt.plot([e - d1["eFermi"] for e in d1["energy"]], d1["dos(up)"], 'c')
#plt.plot([e - d1["eFermi"] for e in d1["energy"]], [-d for d in d1["dos(dn)"]], 'c')
#plt.plot([e - d2["eFermi"] for e in d2["energy"]], d2["dos(up)"], 'g')
#plt.plot([e - d2["eFermi"] for e in d2["energy"]], [-d for d in d2["dos(dn)"]], 'g')


#plt.legend()
#plt.xlabel(r"$E-E_\mathrm{F}$ (eV)")
#plt.ylabel("Electronic DOS")
#plt.xlim(-5, 5)
#plt.ylim(-15, 15)
#plt.savefig(SAVE_LOC + "sv0Strain.pdf")






            






    
