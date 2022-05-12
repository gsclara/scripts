# Clara Garcia Sanchez
# 03/02/2022
# Ploting probes results from openfoam using readProbes
#
# Functions in use
#       output = readLinesOF(ftype, nlines, ntimes, nfolder , nfile)
# Last Modified: 16/07/2019
#--------------------------------------------------------------------------------------------------------#
# Libraries
#--------------------------------------------------------------------------------------------------------#
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib.cm import get_cmap
#--------------------------------------------------------------------------------------------------------#
# CFD results
#--------------------------------------------------------------------------------------------------------#
iteration=[]
p=[]
Ux=[]
Uy=[]
Uz=[]
k=[]
epsilon=[]
nfolder = '/Users/claragarciasan/Documents/TUD/Research/emptyDomainsCFD/rectangularMesh/postProcessing/residuals/0'
nfile = 'residuals.dat'
with open(nfolder+'/'+nfile, encoding="utf8", errors='ignore') as f:
    lines = f.readlines()[2:]
    c=0
    for line in lines:
        c+=1
        fields = np.array(line.split())
        iteration.append(float(fields[0]))
        p.append(float(fields[1]))
        Ux.append(float(fields[2]))
        Uy.append(float(fields[3]))
        Uz.append(float(fields[4]))
        k.append(float(fields[5]))
        epsilon.append(float(fields[6]))
    f.close()
#--------------------------------------------------------------------------------------------------------#
# Plotting
#--------------------------------------------------------------------------------------------------------#
fig= plt.figure(figsize=(10,6))
ax1 = fig.add_subplot(111)
ax1.plot(p,'k-')
ax1.plot(iteration,Ux,'b-')
ax1.plot(iteration,Uy,'c-')
ax1.plot(iteration,Uz,'g-')
ax1.plot(iteration,k,'m-')
ax1.plot(iteration,epsilon,'y-')
ax1.set_xlabel('iterations',fontsize=14)
ax1.set_ylabel('Residuals',fontsize=14)
ax1.legend(['p','Ux','Uy','Uz','k','epsilon'],loc ="upper right")
plt.show()
