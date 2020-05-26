# Density of States (definitly electronic, maybe phonons later)

import matplotlib.pyplot as plt
import DensityOfStatesHeader as dos

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.tight_layout = True

DOSCAR_LOC = "C://Users//baron//Desktop//DOSCAR"
POSCAR_LOC = "C://Users//baron//Desktop//POSCAR"
SAVE_LOC = "C://Users//baron//Desktop//"

#MAIN------------------------------------------------------------------------    
head = dos.ReadDoscarHead(DOSCAR_LOC)
fullDosData = dos.GetEnergyInfo(DOSCAR_LOC, 0) ##0th atom corresponds to the full system
fullDosValues = dos.GetAtomDosInfo(DOSCAR_LOC, 0)

eFermi = fullDosData["eFermi"]
nedos = fullDosData["NEDOS"]
energies = fullDosValues["energy"]
fullDos = fullDosValues["dos"]

ranges = dos.ScanPoscar(POSCAR_LOC)
for r in ranges:
    mi = dos.AtomGroup(DOSCAR_LOC, r[1], nedos, atomType = r[0])
    mi.PlotThisAtom()

plt.legend()
plt.xlabel(r"$E-E_\mathrm{F}$ (eV)")
plt.ylabel("Electronic DOS")
#plt.xlim(-13.5, -9.5)
plt.ylim(0)
plt.savefig(SAVE_LOC + "full.pdf")






            






    
