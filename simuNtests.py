# lance simulations pour different nombre d'electeurs
import multiprocessing
import os, sys
import shutil
import time
import numpy as np
from randomSets import *


def worker(((Ncandidats,q, Nwinners))):
    """worker function"""
    sys.stdout.write('\nSTART -- %i candidats -- \n' % Ncandidats)
    sys.stdout.flush()
    time.sleep(0.01) # being sure that simulation are differently initialized
    minNvoters =  simulate(Ncandidats, q =q, Nwinners = Nwinners)
    with open('nmin-candidates-%i' % Ncandidats,'a') as f_handle:
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

    Ncandidates = int(sys.argv[1])
    Ntests = [sys.argv[1] if len(sys.argv) == 3 else 1000]
    Nwinners = 1
    args = []
    print Ncandidates
    for i in range(Ntests):
        arg = [Ncandidates,100,1]
        args.append(arg)
    if args == []:
        print "Rien a faire!"
    pool       = multiprocessing.Pool(processes=20)
    pool.map(worker, args)

    print "Alors, ca marche ? :)"
