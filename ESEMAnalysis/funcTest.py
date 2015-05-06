import numpy as np

x = y = z = np.arange(0.0,5.0,1.0)
z = np.arange(0.0,5.0,0.5)
dataFileName = 'a.txt'
f = open(dataFileName,'w')
f.write(" ".join(str(elem) for elem in z) + "\n")
f.close()
np.savetxt('test.txt', x, delimiter=',')   # X is an array
#np.savetxt('test.txt', (x,y,z))   # x,y,z equal sized 1D arrays
#np.savetxt('test.txt', x, fmt='%1.4e')   # use exponential notation
