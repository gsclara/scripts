# Clara Garcia-Sanchez
# 04/07/2022
# compute grid convergence index test
# validation based on "Procedure for estimation and reporting or uncertainty
# due to discretization in CFD applications, Celik et al. 2008"
# For 3D: h = 1/N*sum(1,N)(ΔVi)^(1/3)
# where ΔVi is the volume, and N is the total number of cells used for the computations
# phi = field of interest
# Last Modified: 05/07/2022
import numpy as np
from GCI import *

# # Test values
h1 = 2
h2 = 3
h3 = 4
phi1 = 6.063
phi2 = 5.972
phi3 = 5.863
order = 2
step = 0.1

(p,ea,eext,GCIvalue)=GCI(h1,h2,h3,phi1,phi2,phi3,order,step)
print(p,ea,eext,GCIvalue)
