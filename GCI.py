# Clara Garcia-Sanchez
# 04/07/2022
# compute grid convergence index
# implementation based on "Procedure for estimation and reporting or uncertainty
# due to discretization in CFD applications, Celik et al. 2008"
#
# -Usage-
#	(p,ea,eext,GCI) = GCI(h1,h2,h3,phi1,phi2,phi3,order,step)
# -Inputs-
#	h1,h2,h3: representative cell sizes
#	phi1,phi2,phi3: field of interest (normally a point)
#	order: final order
#	step:
#
# -Outputs-
#	p: apparent order
#	ea: approximate relative error
#	eext: extrapolated relative error
#	GCI: fine-grid convergency index

# Last Modified: 05/07/2022
import numpy as np

# # Test values
# r21 = 1.5
# r32 = 1.333
# phi1 = 6.063
# phi2 = 5.972
# phi3 = 5.863

def GCI(h1,h2,h3,phi1,phi2,phi3,order,step):

	# step 2: compute relation between different meshes
	r21 = h2/h1
	r32 = h3/h2

	# step 3: compute apparent order
	epsilon32 = phi3-phi2
	epsilon21 = phi2-phi1
	s = 1*np.sign(epsilon32/epsilon21)
	p_guess = np.linspace(step,order,order/step)
	p_computed = p_guess*0
	# print(p)
	#print(p_guess[1])

	for i in range(0,20):
		q = np.log((r21**p_guess[i]-s)/(r32**p_guess[i]-s))
		p_computed[i] = 1/np.log(r21)*np.abs(np.log(np.abs(epsilon32/epsilon21))+q)
	p_error = p_computed-p_guess
	# print(p[np.argmin(np.abs(p_error))])

	p = p_computed[np.argmin(np.abs(p_error))]
	phi_ext = (r21**p*phi1-phi2)/(r21**p-1)
	ea = np.abs((phi1-phi2)/phi1)
	eext=np.abs((phi_ext-phi1)/phi_ext)
	GCIvalue=1.25*ea/(r21**p-1)

	return(p,ea*100,eext*100,GCIvalue*100)
