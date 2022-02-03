# Clara Garcia-Sanchez
# 16/07/2019
# read OpenFOAM probes function
#
# -Usage-
#	output = readProbesOF(ftype, nprobes, ntimes, nfolder , nfile)
# -Inputs-
#	ftype: field type (scalar/vector)
#   nprobes: number of probes
#   ntimes: number of points/tims extracted from the CFD
#   nfolder: name of the folder where the data is storaged
#   nfile: name file to be read
#
# -Outputs-
#	outputs (1: scalar)
#	outputs (3: vector)
# Last Modified: 16/07/2019

# Function that reads probes following the input parameters selected
import numpy as np
def readProbesOF(ftype, nprobes, ntimes, nfolder , nfile):
	if ftype=="scalar":
		output=np.zeros((ntimes,nprobes))
		c=0; iE=0; time=[]
		with open(nfolder+'/'+nfile, encoding="utf8", errors='ignore') as f:
			for line in f:
				c+=1
				fields = line.split()
				if c > nprobes+2:
					time.append(float(fields[0]))
					output[iE,:]=fields[1:len(fields[:])]
					iE+=1
		f.close()
		time=np.array(time)
		output=np.array(output)
		return (output,time)
	elif ftype=="vector":
		output1=np.zeros((ntimes,nprobes)) 
		output2=np.zeros((ntimes,nprobes)) 
		output3=np.zeros((ntimes,nprobes)) 
		c=0; iE=0; time=[]
		with open(nfolder+'/'+nfile, encoding="utf8", errors='ignore') as f:
			for line in f:
				c+=1
				fields = line.split()
				if c > nprobes+2:
					time.append(float(fields[0]))
					output1[iE,:]=fields[1:len(fields[:]):3]
					output2[iE,:]=fields[2:len(fields[:]):3]
					output3[iE,:]=fields[3:len(fields[:]):3]
					iE+=1
		f.close()
		time=np.array(time)
		output1=np.array(output1)
		output2=np.array(output2)
		output3=np.array(output3)
		return (output1,output2,output3,time)
	else:
		print("type does not exist")
		return
