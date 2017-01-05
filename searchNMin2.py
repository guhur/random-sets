from randomSets import *
import numpy as np

winners = [1,5,10]
candidates = range(100, 1100, 500)
Nmin = np.zeros((len(winners),len(candidates)))
for i in range(len(winners)):
    for j in range(len(candidates)):
        print("Nwinner: %i, Ncandidates: %i" % (winners[i], candidates[j]))
        #alpha = findMinAlpha(Ncandidates, Nvoters, Ntests = 100, Nsubset = 5, q = 1, alphaMin = 1, epsilon1=0.1, epsilon2=0.1)
        Nmin[i,j] = findMinNvoters(candidates[j], Nwinner = winners[i], Nsubset = 5, Ngrades = 5, q = 5000, alpha = 2, Ntests=500)
        print("Nmin: %i\n" % Nmin[i,j])

np.savetxt('nmin-winners-1-5-10-candidates-100-to-1000.txt', Nmin)

