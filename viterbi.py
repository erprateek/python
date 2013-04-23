import math
import numpy as np
def decode(seqFile, I, B, A):
    T = len(seqFile)
    VP = np.zeros((N,T), dtype=float)
    char_init = seqFile[0]
    cInd = ord(char_init)-ord(baseChar)
    for i in range(N):
        if (B[cInd][i] > 0 and I[0][i] != 0):   VP[i][0] = math.log10(I[0][i]) + math.log10(B[cInd][i])
        else:   VP[i][0] = -10000000.0
    timestep = []
    ind_mat = []
    print "VP initialized "
    print VP
    for t in range(1,T):        #For each word in the sequence/ or the timestep
        for i in range(N):
            for j in range(N):
                cIndex = ord(seqFile[t])-ord(baseChar)
                prev_state = VP[j][t-1]
                trans = A[j][i]
                print "JI", j,i
                if B[cIndex][i] > 0 and prev_state > -50000 and trans > 0:
                    calc = prev_state+math.log10(trans)+math.log10(B[cIndex][i])
                else:   calc = -10000000.000000000000
                timestep.append(calc)
        print "Timestep", t , "the values are", timestep
        VP[0][t] = max(timestep[0],timestep[1])
        VP[1][t] = max(timestep[2],timestep[3])
        timestep = []
    for t in range(T):     
        if VP[0][t] <= VP[1][t]:    ind_mat.append((1,t))
        else:   ind_mat.append((0,t))
    ind_mat.sort(key=lambda tup: tup[1])
    states = [x[0] for x in ind_mat]
    result = zip(seqFile,states)
    for (x,y) in result:     print x,y    

if __name__ == '__main__':
    f = open("samplemod2")
    g = open("sampleseq2")
    r = f.read().splitlines()
    seqFile = g.read().splitlines()
    N = int(r[0])
    baseChar = '!'
    SYMNUM = 94
    I = np.zeros((1,N))
    B = np.zeros((SYMNUM,N))
    A = np.zeros((N,N))
    for keywrd in r:
        if keywrd.startswith("InitPr"):
            ind = r.index(keywrd)
            ind_parse = r[ind].split(' ')
            count = int(ind_parse[1])
            st_ind = ind+1
            for line in xrange(st_ind, st_ind+count):
                index = int(r[line].split(" ")[0])
                val = float(r[line].split(" ")[1])
                I[0][index] = val
        if keywrd.startswith("OutputPr"):
            ind = r.index(keywrd)
            ind_parse = r[ind].split(' ')
            count = int(ind_parse[1])
            st_ind = ind+1
            for line in xrange(st_ind, st_ind+count):
                (s,sym,pr) = r[line].split(" ")
                s = int(s)
                pr = float(pr)
                calc = ord(sym)-ord(baseChar)
                B[calc][s] = pr
        if keywrd.startswith("TransPr"):
            ind = r.index(keywrd)
            ind_parse = r[ind].split(' ')
            count = int(ind_parse[1])
            st_ind = ind+1
            for line in xrange(st_ind, st_ind+count):
                (s,s1,pr) = r[line].split(" ")
                A[int(s)][int(s1)]=float(pr)
    decode(seqFile,I, B, A)
