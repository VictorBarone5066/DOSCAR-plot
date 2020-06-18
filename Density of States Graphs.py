# Density of States (definitly electronic, maybe phonons later)

import matplotlib.pyplot as plt
import DensityOfStatesHeader as dos

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.tight_layout = True

DOSCAR_LOC = "C://Users//baron//Desktop//DOSCAR"
POSCAR_LOC = "C://Users//baron//Desktop//POSCAR"
SAVE_LOC = "C://Users//baron//Desktop//"


# <codecell> main ------------------------------------------------------------------------    
#Examples of how to use header file:


#Plot full DOS for non-spin polarized--------------------------------------------------------------
fullDosData = dos.GetEnergyInfo(DOSCAR_LOC, 0) ##0th atom corresponds to the full system
vals = dos.GetAtomDosInfo(DOSCAR_LOC, 0, spin=False)
plt.plot([e - fullDosData["eFermi"] for e in vals["energy"]], vals["dos"], 'k', linewidth = .85)
plt.legend()
plt.xlabel(r"$E-E_\mathrm{F}$ (eV)")
plt.ylabel(r"Electronic DOS (states / eV)")
plt.xlim(-5, 5)
plt.ylim(0)
plt.savefig(SAVE_LOC + "dos.pdf")


#Plot Full DOS for spin-polarized------------------------------------------------------------------
eFermi = dos.GetEnergyInfo(DOSCAR_LOC, 0)["eFermi"]
vals = dos.GetAtomDosInfo(DOSCAR_LOC, 0, spin = True)
plt.plot([e - eFermi for e in vals["energy"]], vals["dos(up)"], 'k', linewidth = .85)
plt.plot([e - eFermi for e in vals["energy"]], [-d for d in vals["dos(dn)"]], 'k', linewidth = .85)
plt.legend()
plt.xlabel(r"$E-E_\mathrm{F}$ (eV)")
plt.ylabel(r"Electronic DOS (states / eV)")
plt.xlim(-5, 5)
plt.savefig(SAVE_LOC + "dos.pdf")


#Plot Partial DOS for all atoms (explicitly C atoms), without the D orbital, spin polarized--------
nAtoms = dos.ReadDoscarHead(DOSCAR_LOC)["nAtoms"]
nedos = dos.GetEnergyInfo(DOSCAR_LOC, 0)["NEDOS"]
    #the [1, nAtoms] below tells the function to add up all of the PDOS for each atom
allDos = dos.AtomGroup(DOSCAR_LOC, [1, nAtoms], nedos, spin = True, atomType = 'C')
allDos.PlotThisAtom(suppressD = True)
plt.xlabel(r"$E-E_\mathrm{F}$ (eV)")
plt.ylabel(r"Electronic PDOS (states / eV)")
plt.ylim(-.2, .2)
plt.savefig(SAVE_LOC + "pdos.pdf")


#Plot local (around 3 C atoms in this case) partial DOS for spin polarized--------------------------
nedos = dos.GetEnergyInfo(DOSCAR_LOC, 0)["NEDOS"]
        ##the [0] in the below function call does not do anything.  The function, if supplied with 'atomVals',
        ##uses those instead of atomRange (which is what the [0] is being assigned to).  
ldos = dos.AtomGroup(DOSCAR_LOC, [0], nedos, atomVals = [8, 11, 64], atomType = 'C', spin = True)
ldos.PlotThisAtom(suppressD = True) #hide the D orbital from this graph
plt.legend()
plt.xlabel(r"$E-E_\mathrm{F}$ (eV)")
plt.ylabel(r"LPDOS (states / eV $\cdot$ atom)")
plt.xlim(-5, 5)
plt.ylim(-0.4, 0.4)
plt.savefig(SAVE_LOC + "lpdos.pdf")


#Plot the summed PDOS of each atom type for non-spin polarized.  Requires corresponding POSCAR-----
ranges = dos.ScanPoscar(POSCAR_LOC) #returns a list of atom types and their ranges
nedos = dos.GetEnergyInfo(DOSCAR_LOC, 0)["NEDOS"]
for r in ranges: #For each atom, generate an atom group with atom ranges defined by the above function...
    mi = dos.AtomGroup(DOSCAR_LOC, r[1], nedos, atomType = r[0])
    mi.PlotThisAtom()#... and add them to plots
plt.legend()
plt.xlabel(r"$E-E_\mathrm{F}$ (eV)")
plt.ylabel(r"PDOS (states / eV)")
plt.xlim(-5, 5)
plt.ylim(0)
plt.savefig(SAVE_LOC + "lpdos.pdf")










            






    
