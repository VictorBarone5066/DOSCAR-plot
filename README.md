# DOSCAR-plot
Python code for analysis of VASP DOSCAR files 

The header file contains functions for most of what you'll need for plotting.  In the order of (important) functions / classes:
  ScanPoscar():
    INPUT:  the location of a VASP POSCAR file
    OUTPUT: a list of ion types and the ranges of atom numbers that each ion is in.  The format is
            [[ion 1, [first ion 1 number, last ion 1 number]], [ion 2, [first ion 2 number, last ion 2 number]], etc...]
  AtomGroup:
    Class that helps make the plotting of individual atom types less cumbersome.  Contains s-, p-, d-, DOS values in lists parallel 
    to energy.  These lists are the sum of each individual atom's DOS for a given range of atoms.  
    Initialization:
      Necessary: Location of DOSCAR, the (inclusive) range of atoms you want (counting starts at 1), NEDOS
      Optional:  The label that you want (meant to be the atom's name), whether spin-polarization was used (assumed false)
      
  GetAtomDosInfo():
    INPUT:  DOSCAR file location, atom number, spin polarization (assumed to be false)
    OUTPUT: A Dict. containing DOS information for the atom whose atom number was supplied.  
    **Note that supplying atom number = 0 means that the output will give you information about the entire system instead of an individual
    atom.  
    
    **Note:  Supplying spin polarization = true will instead give values for spin-up and spin-down DOS.  The code does NOT automatically
    determine whether spin polarization was used (yet), so not supplying the right information will lead to some strange results. 
