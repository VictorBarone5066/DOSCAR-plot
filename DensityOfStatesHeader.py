from matplotlib import pyplot as plt

#Hope you don't somehow have more than 8 atom types in a POSCAR file
COLORS = [(0, 0, 0), #black
          (255, 0, 0), #red
          (0, 173, 0), #(better) green
          (0, 0, 255), #blue
          (255, 0, 183), #pink
          (15, 243, 255), #cyan
          (235, 109, 0), #orange
          (153, 0, 235) #purple
          ]
cIndex = 0

def GetColor(i):
    return (a / 255 for a in COLORS[i])

#returns a 2D array, where each element is a pair of [atom type, range], where range is in the form [low, high] inclusive
def ScanPoscar(inLoc, atomTypeLineNum = 5, atomNumLineNum = 6):
    atomTypes, atomTypeNums, ret = [], [], []
    
    with open(inLoc) as infile:
        for i, line in enumerate(infile):
            if (i == atomTypeLineNum):
                for a in line.split():
                    atomTypes.append(a)
            if (i == atomNumLineNum):
                for a in line.split():
                    atomTypeNums.append(int(a))
                infile.close()
                break    
    
    #Don't worry about how this works - it was mostly luck on my part anyways
    tot = sum(atomTypeNums)
    ret.append([atomTypes[0], [1, atomTypeNums[0]]])
    tot= tot - atomTypeNums[0]
    i = 1
    while(tot > 0):
        ret.append([atomTypes[i], [ret[i-1][1][1] + 1, ret[i-1][1][1] + atomTypeNums[i]]])
        tot = tot - atomTypeNums[i]
        i = i + 1
        
    return ret

class AtomGroup:
    atomType = None
    nAtoms = None
    dosData = None
    spin = None
    
    energy = None
    sDosSum = None
    pDosSum = None
    dDosSum = None

    sUpDosSum = None
    sDnDosSum = None    
    pUpDosSum = None
    pDnDosSum = None
    dUpDosSum = None
    dDnDosSum = None
    
    def __init__(self, inLoc, atomRange, nedos, spin = False, atomType = "???"):
        if(len(atomRange) != 2):
            print("AtomGroup Initialize:  atomRange needs two values, in list form: [low, high].  The numbers are inclusive.\n")
            return
        if(atomRange[0] == 0):
            print("AtomGroup Initialize:  This class only supports atom data, and atom 0 is designated as the full system DOS.  The first atom is atom 1, and so on.\n")
            return
        
        self.atomType = atomType
        self.nAtoms = (atomRange[-1] - atomRange[0] + 1)
        self.dosData = []
        self.spin = spin
        
        i = atomRange[0]
        energies, dosS, dosP, dosD, dosSu, dosPu, dosDu, dosSd, dosPd, dosDd = [], [], [], [], [], [], [], [], [], []
        while(i <= atomRange[-1]):
            thisAtom = GetAtomDosInfo(inLoc, i, self.spin)
            self.dosData.append(thisAtom)
            energies.append(thisAtom["energy"])
            
            if (not self.spin):
                dosS.append(thisAtom["sDos"])
                dosP.append(thisAtom["pDos"])
                dosD.append(thisAtom["dDos"])    
            if(self.spin):
                dosSu.append(thisAtom["sDos"])
                dosPu.append(thisAtom["pDos"])
                dosDu.append(thisAtom["dDos"])                 
                dosSd.append(thisAtom["sDos"])
                dosPd.append(thisAtom["pDos"])
                dosDd.append(thisAtom["dDos"])             
            
            i = i + 1

        i = 0
        self.sDosSum, self.pDosSum, self.dDosSum = [0]*nedos, [0]*nedos, [0]*nedos
        self.sUpDosSum, self.pUpDosSum, self.dUpDosSum = [0]*nedos, [0]*nedos, [0]*nedos
        self.sDnDosSum, self.pDnDosSum, self.dDnDosSum = [0]*nedos, [0]*nedos, [0]*nedos        
        self.energy = energies[0]

        while(i < (atomRange[-1] - atomRange[0] + 1)):
            j = 0
            while(j < len(energies[i])):
                if (not self.spin):
                    self.sDosSum[j] = self.sDosSum[j] + dosS[i][j]
                    self.pDosSum[j] = self.pDosSum[j] + dosP[i][j]   
                    self.dDosSum[j] = self.dDosSum[j] + dosD[i][j]
                if(self.spin):
                    self.sUpDosSum[j] = self.sUpDosSum[j] + dosSu[i][j]
                    self.pUpDosSum[j] = self.pUpDosSum[j] + dosPu[i][j]   
                    self.dUpDosSum[j] = self.dUpDosSum[j] + dosDu[i][j]
                    self.sDnDosSum[j] = self.sDnDosSum[j] + dosSd[i][j]
                    self.pDnDosSum[j] = self.pDnDosSum[j] + dosPd[i][j]   
                    self.dDnDosSum[j] = self.dDnDosSum[j] + dosDd[i][j]                    
                j = j + 1
            i = i + 1        

    def PlotThisAtom(self, suppressS = False, suppressP = False, suppressD = False):
        global cIndex
        cIndex = (cIndex + 1)%8
        if(not suppressS):
            plt.plot([e - self.dosData[0]["eFermi"] for e in self.energy], self.sDosSum, color=tuple(GetColor(cIndex)), label=self.atomType+" "+'(s)', linewidth=.8)
        if(not suppressP):
            plt.plot([e - self.dosData[0]["eFermi"] for e in self.energy], self.pDosSum, color=tuple(GetColor(cIndex)), label=self.atomType+" "+'(p)', linewidth=.8, linestyle='--')
        if (not suppressD):
            plt.plot([e - self.dosData[0]["eFermi"] for e in self.energy], self.dDosSum, color=tuple(GetColor(cIndex)), label=self.atomType+" "+'(d)', linewidth=.8, linestyle=':')


def GetNEDOS(inLoc):
    with open(inLoc) as infile:
        for i, line in enumerate(infile):
            if (i == 5):
                infile.close()
                break
    return int((line.split())[2]) 

def GetLineRange(atomNum, NEDOS):    
    if(atomNum < 1):
        return [5, 5+NEDOS]
    #[low, high]
    return [5+atomNum*(1+NEDOS), 5+atomNum+(atomNum+1)*NEDOS]
    

def ReadDoscarHead(inLoc):
    ret = {"nAtoms": None,
           "PDOS": None}
    
    lines = []
    with open(inLoc, 'r') as infile:
        for line in infile:
            lines.append(line)
            if(len(lines) > 4):
                infile.close()
                break    

    ret["nAtoms"] = int((lines[0].split())[0])
    ret["PDOS"] = bool((lines[0].split())[2])
    return ret
    
def GetEnergyInfo(inLoc, atomNum):
    ret = {"eMax": None,
           "eMin": None,
           "NEDOS": None,
           "eFermi": None}
    
    lineRange = GetLineRange(atomNum, GetNEDOS(inLoc))
    
    with open(inLoc) as infile:
        for i, line in enumerate(infile):
            if (i == lineRange[0]):
                infile.close()
                break
            
    ret["eMax"] = float((line.split())[0])
    ret["eMin"] = float((line.split())[1])
    ret["NEDOS"] = int((line.split())[2])        
    ret["eFermi"] = float((line.split())[3])
    return ret

def GetAtomDosInfo(inLoc, atomNum, spin = False):
    #Need cases for spin-pol and cases for getting specific atoms or the entire system.
    #General:
    ret = {"type" : None, #all cases.  For determining what is inside ret.  see below
           "eFermi": None, #all cases
           "energy": None, #all cases
           "dos": None, #entire system, spin pol off
           "dos(up)" : None, #entire system, spin pol on
           "dos(dn)" : None, #entire system, spin pol on
           "intDos": None, #entire system, spin pol on
           "intDos(up)" : None, #entire system, spin pol on
           "intDos(dn)" : None, #entire system, spin pol on      
           "sDos" : None, #specific atom, spin pol off
           "pDos" : None, #specific atom, spin pol off
           "dDos" : None, #specific atom, spin pol off
           "sDos(up)" : None,#<-|
           "sDos(dn)" : None,#<-|
           "pDos(up)" : None,    #specific atom, spin pol on
           "pDos(dn)" : None,#<-|
           "dDos(up)" : None,#<-|
           "dDos(dn)" : None #<-|                     
           }  
    eInfo = GetEnergyInfo(inLoc, atomNum)
    NEDOS_ = eInfo["NEDOS"]
    eFermi_ = eInfo["eFermi"]   
    lineRange = GetLineRange(atomNum, NEDOS_)
    
    ret["eFermi"] = eFermi_ 
    
    #TYPE 0: entire system, spin pol off:
    if(atomNum < 1 and not spin):
        e, d, iD = [], [], [] #energy, dos, integrated dos
        infile = open(inLoc, 'r')
        for i, line in enumerate(infile):
            if (lineRange[0] < i <= lineRange[1]):
                e.append(float(line.split()[0]))
                d.append(float(line.split()[1]))    
                iD.append(float(line.split()[2])) 
        infile.close()
       
        ret["type"] = 0
        ret["energy"] = e    
        ret["dos"] = d
        ret["intDos"] = iD
    
    #TYPE 1: entire system, spin pol on:
    if(atomNum < 1 and spin):
        e, du, dd, iDu, iDd = [], [], [], [], [] #energy, dos up & down, int dos up & down
        infile = open(inLoc, 'r')
        for i, line in enumerate(infile):
            if (lineRange[0] < i <= lineRange[1]):
                e.append(float(line.split()[0]))
                du.append(float(line.split()[1]))    
                dd.append(float(line.split()[2])) 
                iDu.append(float(line.split()[3]))    
                iDd.append(float(line.split()[4]))             
        infile.close()
       
        ret["type"] = 1
        ret["energy"] = e    
        ret["dos(up)"] = du
        ret["dos(dn)"] = dd
        ret["intDos(up)"] = iDu   
        ret["intDos(dn)"] = iDu     

    #TYPE 2: specific atom, spin pol off:
    if(atomNum >= 1 and not spin):    
        e, s, p, d = [], [], [], [] #energy, s-dos, p-dos, d-dos
        infile = open(inLoc, 'r')
        for i, line in enumerate(infile):
            if (lineRange[0] < i <= lineRange[1]):
                e.append(float(line.split()[0]))
                s.append(float(line.split()[1]))    
                p.append(float(line.split()[2])) 
                d.append(float(line.split()[3]))                
        infile.close()
       
        ret["type"] = 2
        ret["energy"] = e    
        ret["sDos"] = s
        ret["pDos"] = p
        ret["dDos"] = d   
    
    #TYPE 3: specific atom, spin pol on:   (yikes)
    if(atomNum >= 1 and spin):
        e, su, sd, pu, pd, du, dd = [], [], [], [], [], [] #energy, s-dos up/dn, p-dos up/dn, d-dos up/dn
        infile = open(inLoc, 'r')
        for i, line in enumerate(infile):
            if (lineRange[0] < i <= lineRange[1]):
                e.append(float(line.split()[0]))
                su.append(float(line.split()[1]))    
                sd.append(float(line.split()[2])) 
                pu.append(float(line.split()[3]))  
                pd.append(float(line.split()[4]))    
                du.append(float(line.split()[5])) 
                dd.append(float(line.split()[6]))               
        infile.close()
       
        ret["type"] = 3
        ret["energy"] = e    
        ret["sDos(up)"] = su
        ret["sDos(dn)"] = sd
        ret["pDos(up)"] = pu
        ret["pDos(dn)"] = pd 
        ret["dDos(up)"] = du
        ret["dDos(dn)"] = dd    
    
    return ret


