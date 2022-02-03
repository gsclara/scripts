# Clara Garcia-Sanchez
# 16/07/2019
# read OpenFOAM lines function
#
# -Usage-
#	output = readLinesOF(ftype, npoints, ndim, nfolder , nfile)
# -Inputs-
#	ftype: field type (scalar/vector)
#   npoints: number of lines
#   ndim: in case the input is a scalar
#   nfolder: name of the folder where the data is storaged
#   nfile: name file to be read
#
# -Outputs-
#	outputs (ndim, values)

# Last Modified: 03/02/2022

# Function that reads lines following the input parameters selected
import numpy as np
def readLinesOF(npoints, ndim, nfolder , nfile):
	output=np.zeros((ndim+1,npoints))
	c=0; iE=0
	with open(nfolder+'/'+nfile, encoding="utf8", errors='ignore') as f:
		for line in f:
			c+=1
			fields = line.split()
			output[:,iE]=fields
			iE+=1
	f.close()
	return(output)
# nfolder='/Users/claragarciasan/Documents/TUD/Research/WallFunction2D/emptyDomainkEpsilonParente/postProcessing/linesInOut/0'
# nfile='lineIn_U.xy'
# npoints=100
# output=np.zeros((4,npoints))
# c=0; iE=0;
# with open(nfolder+'/'+nfile, encoding="utf8", errors='ignore') as f:
# 	for line in f:
# 		c+=1
# 		fields = line.split()
# 		output[:,iE]=fields
# 		iE+=1
# f.close()

# nfolder='/Users/claragarciasan/Documents/TUD/Research/WallFunction2D/emptyDomainkEpsilonParente/postProcessing/linesInOut/0'
# nfile='lineIn_epsilon_k.xy'
# npoints=100
# nscalar=2
# output=np.zeros((nscalar+1,npoints))
# c=0; iE=0;
# with open(nfolder+'/'+nfile, encoding="utf8", errors='ignore') as f:
# 	for line in f:
# 		c+=1
# 		fields = line.split()
# 		output[:,iE]=fields
# 		iE+=1
# f.close()
# print(output)

