import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('font',**{'family':'serif','serif':['Times']})
rc('text', usetex=True)
import scipy.stats
import sys

# this function builds a random subset
# occurrences must an np.array with dtype=float
def subset(Ncandidates, Nsubset, occurrences, alpha = 1.0):
    proba_candidat = np.array([1/(j**alpha) if j != 0 else 1 for j in occurrences])
    proba_candidat = proba_candidat / float(sum(proba_candidat))
    lot = np.random.choice(Ncandidates, size=Nsubset, replace=False, p=proba_candidat)
    occurrences[lot] += 1
    return lot


def vote(lot, proba, Nsubset, Ngrades):
    votes = np.zeros(Nsubset, dtype=int)
    for i in range(Nsubset):
        votes[i] = np.random.choice(range(Ngrades), size=1, replace=True, p=proba[i])
    return votes

def normalize(v, ax=1):
    n = np.sum(v, axis=ax)
    b = np.transpose(v)
    c = np.divide(b,n)
    return np.transpose(c)

def tieBreaking(A, B):
    #print str(A) + " " + str(B)
    Ac = np.copy(A)
    Bc = np.copy(B)
    medA = argMedian(Ac)
    medB = argMedian(Bc)
    while medA == medB:
        Ac[medA] -= 1
        Bc[medB] -= 1
        if not any(Ac):
            return -1
        if not any(Bc):
            return 1
        medA = argMedian(Ac)
        medB = argMedian(Bc)
    return -1 if (medA < medB) else 1

def majorityJudgment(results):
    return sorted(range(len(results)), cmp=tieBreaking, key=results.__getitem__)

def probaCandidates(Ncandidates, Ngrades, inFile):
    """Read inFile. If there is not enough candidates, interpolate other. Save in outFile """
    inCandidates = np.genfromtxt(inFile, delimiter = " ", dtype=float)
    inCandidates = inCandidates[:,:Ngrades]
    Nc = len(inCandidates)
    N  = min(Nc, Ncandidates)
    param = np.zeros((Ngrades,2))
    param[:,0] = np.mean(inCandidates, axis=0)
    param[:,1] = np.std(inCandidates, axis=0)
    np.random.shuffle(inCandidates)
    outCandidates = np.zeros((Ncandidates,Ngrades))
    outCandidates[:N] = inCandidates[:N,:]
    if Ncandidates > Nc:
        for i in range(Ngrades):
            outCandidates[N:,i] = np.random.normal(param[i,0], param[i,1], Ncandidates-Nc)
    return normalize(np.absolute(outCandidates))

def argMedian(A):
    Ngrades = len(A)
    s   = np.array([sum(A[:i+1]) for i in range(Ngrades)])
    mid = float(s[Ngrades-1])/2
    return np.argwhere(mid < s)[0][0]


def rankError(rk_priori, rk_post, N):
    rk  = np.concatenate((rk_priori[:N], rk_post[:N]))
    return len(set(rk)) - N


def findMinNvoters(Ncandidates, maxError = 0.1, Ntests = 100, Nwinner = 1, Nsubset = 5, Ngrades = 5, q = 1000, alpha = 1, real_results = "terranova.txt", epsilon=0.0):
    if epsilon == 0.0:
        epsilon = maxError/10 # not implemented yet
    maxTests = Ntests # max number of tests
    Nvoters = 0
    Nvoters_old = 0
    error = maxError + 1

    # perfect election
    pr_priori = probaCandidates(Ncandidates, Ngrades, real_results)
    res_priori = np.trunc(pr_priori*1000)
    rk_priori = majorityJudgment(res_priori)

    # election with random sets
    raw = np.zeros((Ntests, Ncandidates,Ngrades))
    occurrence = np.zeros((Ntests, Ncandidates))
    while error > maxError:
        Nvoters += q
        sys.stdout.write("\r%i voters is too low (%.4f > %.4f). Try with %i voters.\n" % (Nvoters_old, error, maxError, Nvoters))
        err_samples = np.zeros(Ntests, dtype=int)
        for t in range(Ntests):
            sys.stdout.write("\rTest: %i/%i (%i %%)" % (t+1, Ntests, float(t)/float(Ntests)*100.0))
            for i in range(Nvoters_old, Nvoters+1):
                lot     = subset(Ncandidates, Nsubset, occurrence[t], alpha)
                votes   = vote(lot, pr_priori[lot,:], Nsubset, Ngrades)
                raw[t,lot,votes] += 1
            results = normalize(raw[t])
            rk      = majorityJudgment(raw[t])
            err_samples[t] = rankError(rk_priori, rk, Nwinner)
        error = np.mean(err_samples, axis=0)
        Nvoters_old = Nvoters
    return Nvoters



def computeError(Ncandidates, Nvoters, maxError = 0.1, Nwinner = 1, Nsubset = 5, Ngrades = 5, alpha = 1, real_results = "terranova.txt", epsilon=0.0):
    if epsilon == 0.0:
        epsilon = maxError/10 # not implemented yet
    maxTests = 200 # max number of tests

    # perfect election
    pr_priori = probaCandidates(Ncandidates, Ngrades, real_results)
    res_priori = np.trunc(pr_priori*1000)
    rk_priori = majorityJudgment(res_priori)

    # election with random sets
    raw = np.zeros((maxTests, Ncandidates,Ngrades))
    occurrence = np.zeros((maxTests, Ncandidates))
    err_samples = np.zeros(maxTests, dtype=int)
    for t in range(maxTests):
        for i in range(Nvoters+1):
            lot     = subset(Ncandidates, Nsubset, occurrence[t], alpha)
            votes   = vote(lot, pr_priori[lot,:], Nsubset, Ngrades)
            raw[t,lot,votes] += 1
        results = normalize(raw[t])
        rk      = majorityJudgment(raw[t])
        err_samples[t] = rankError(rk_priori, rk, Nwinner)
    return np.mean(err_samples, axis=0)
