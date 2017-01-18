# lance simulations pour different nombre d'electeurs
import multiprocessing
import os, sys
import shutil
import time
import numpy as np
from randomSets import *


def worker(((Ncandidats,q, Nwinners, Ntests))):
    """worker function"""
    sys.stdout.write('\nSTART -- %i candidats -- \n' % Ncandidats)
    sys.stdout.flush()
    time.sleep(0.01) # being sure that simulation are differently initialized
    minNvoters =  findMinNvoters(Ncandidats, q =q, Nwinners = Nwinners, Ntests = Ntests)
    with open('nmin-candidates-10-to-100-by-2.txt','a') as f_handle:
        f_handle.write("%i " % Ncandidats)
        np.savetxt(f_handle,minNvoters)
    return

if __name__ == '__main__':
    print "Cette fois, c'est la bonne !"
    print (time.strftime("%H:%M:%S"))

    root = "simulations/"
    try:
        os.mkdir(root)
    except OSError:
        pass

    candidates = range(10,110, 2)
    Nwinners = 1
    minNvoters = np.zeros((len(candidates), Nwinners))
    args = []
    for i in range(len(candidates)):
        arg = [candidates[i],200,1,100]
        args.append(arg)
    if args == []:
        print "Rien a faire!"
    pool       = multiprocessing.Pool(processes=20)
    pool.map(worker, args)

    print "Alors, ca marche ? :)"
