from randomSets import *
import numpy as np

import itertools
candidates = range(10,110, 10)
Nwinners = 10
minNvoters = np.zeros((len(candidates), Nwinners))
for i in range(len(candidates)):
    print "C %i " % candidates[i]
    minNvoters[i,:] = findMinNvoters(candidates[i], q =1000, Nwinners = Nwinners, Ntests = 100)
    print minNvoters[i,:]
    np.savetxt('nmin-winners-candidates-10-to-100.txt', minNvoters)
print minNvoters

np.savetxt('nmin-winners-candidates-10-to-100.txt', minNvoters)

