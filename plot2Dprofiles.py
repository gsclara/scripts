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
from readLinesOF import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib.cm import get_cmap
#--------------------------------------------------------------------------------------------------------#
# CFD results
#--------------------------------------------------------------------------------------------------------#
npoints = 100
nfolder = '/Users/claragarciasan/Documents/TUD/Research/WallFunction2D/emptyDomain_2022/postProcessing/linesInOut/2000'
turbulence_In = readLinesOF(npoints, 2, nfolder,'lineIn_epsilon_k.xy')
print(turbulence_In)
velocity_In = readLinesOF(npoints, 3, nfolder,'lineIn_U.xy')
turbulence_Out = readLinesOF(npoints, 2, nfolder,'lineOut_epsilon_k.xy')
velocity_Out = readLinesOF(npoints, 3, nfolder,'lineOut_U.xy')
#--------------------------------------------------------------------------------------------------------#
# Plotting
#--------------------------------------------------------------------------------------------------------#
# Scalars
fig = plt.figure(figsize=(10,6))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax1.plot(turbulence_In[2,:],turbulence_In[0,:],'k-')
ax1.plot(turbulence_Out[2,:],turbulence_Out[0,:],'b-.')
ax1.set_xlabel('k [m^2/s^2]',fontsize=14)
ax1.set_ylabel('Height [m]]',fontsize=14)
ax2.plot(turbulence_In[1,:],turbulence_In[0,:],'k-')
ax2.plot(turbulence_Out[1,:],turbulence_Out[0,:],'b-.')
ax2.set_xlabel('epsilon [m^3/s^2]',fontsize=14)
plt.show()

#Vectors
fig = plt.figure(figsize=(8,6))
ax1 = fig.add_subplot(111)
velocity_magnitude_In = np.sqrt(velocity_In[1,:]*velocity_In[1,:]+velocity_In[2,:]*velocity_In[2,:]+velocity_In[3,:]*velocity_In[3,:])
velocity_magnitude_Out = np.sqrt(velocity_Out[1,:]*velocity_Out[1,:]+velocity_Out[2,:]*velocity_Out[2,:]+velocity_Out[3,:]*velocity_Out[3,:])
ax1.plot(velocity_magnitude_In,velocity_In[0,:],'k-')
ax1.plot(velocity_magnitude_Out,velocity_Out[0,:],'b-.')
ax1.set_xlabel('Velocity Magnitude [m^2/s^2]',fontsize=14)
ax1.set_ylabel('Height [m]',fontsize=14)

plt.show()