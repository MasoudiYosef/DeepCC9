# Dividing the data into training and test sets
def GetData(DSN):
    DT1=open('Data/'+DSN+'.txt','r')
    DT=DT1.readlines()
    DT1.close()
    TRDT=[]
    TEDT=[]
    TRDL=[]
    TEDL=[]
    for i in range(0,round(len(DT)*0.8)):
        k=DT[i].split(',')
        ls=[]
        for j in range(0,len(k)-1):
            ls.append(float(k[j]))
        TRDT.append(ls)
        TRDL.append(float(k[-1]))
    for i in range(round(len(DT)*0.8),len(DT)):
        k=DT[i].split(',')
        ls=[]
        for j in range(0,len(k)-1):
            ls.append(float(k[j]))
        TEDT.append(ls)
        TEDL.append(float(k[-1]))
    return TRDT,TEDT,TRDL,TEDL

# Creating the initial population of candidate solutions
def initial(nob,F,NOF):
    branches=np.zeros([nob,NOF+3])
    for i in range(0,nob):
        for j in range(0,NOF-1):
            branches[i][j]=random.randint(0,F)
        branches[i][NOF-1]=nob
    return branches

# Calculating the fitness of candidate solutions
def score(ARG):
    inx=ARG[0]
    CS=ARG[1]
    global TRDT,TEDT,TRDL,TEDL, SL
    CL=svm.SVR()
    TR=[]
    TD=[]
    for i in range(0,len(TRDT)):
        lst=[]
        for j in range(0,len(CS)-3):
            lst.append(TRDT[i][int(CS[j])])
        TR.append(lst)
    for i in range(0,len(TEDT)):
        lse=[]
        for j in range(0,len(CS)-3):
            lse.append(TEDT[i][int(CS[j])])
        TD.append(lse)
    CL.fit(TR,TRDL)
    PRE=CL.predict(TD)
    RMSD=0
    for i in range(0,len(TD)):
        RMSD=RMSD+pow(TEDL[i]-PRE[i],2)
    print(RMSD)
    SL.append([inx,sqrt(RMSD/len(TD))])

# Use parallel processing to calculate the fitness of candidate solutions
def profit(branches):
    r=len(branches)
    b=len(branches[0])
    global SL
    SL=[]
    THP=[]
    for i in range(0,r):
        TH=threading.Thread(target=score,args=([i,branches[i]],))
        THP.append(TH)
        TH.start()
    for TH in THP:
        TH.join()
    for i in range(0,len(SL)):
        branches[SL[i][0]][b-1]=SL[i][1]
    return branches

# Select the best candidates from the candidate solutions
def SelectBests(branches,nog):
    bests=[]
    c=len(branches[0])-1
    for j in range(0,nog):
        mi=branches[0][c]
        inx=0
        for i in range(1,len(branches)):
            if (branches[i][c]<mi)&(j not in bests):
                inx=i
                mi=branches[i][c]
        bests.append(inx)
    return bests

# Divide the candidate solutions into several groups
def grouping(branches,nog):
    bests=SelectBests(branches,nog)
    c=len(branches[0])-1
    for i in range(0,len(branches)):
        if i in bests:
            branches[i][c-2]=i
        else:
            branches[i][c-2]=bests[random.randint(1,len(bests))-1]
    return branches

# Implementation of the Distributing operator in Trader
def distributing(branches):
    c=len(branches[0])-1
    r=len(branches)
    for i in range(0,r):
        if i != branches[i][c-2]:
            k=random.randint(1,int(round(c*0.2)))
            for j in range(0,k):
                s=int(random.randint(0,c-2))
                branches[i][s]=branches[int(branches[i][c-2])][s]
    return branches

# Implementation of the Retailing operator in Trader
def retailing(branches,itr,AllF,noi):
    c=len(branches[0])-1
    r=len(branches)
    for i in range(0,r):
        k=int(max(1,100-round(itr/noi*100)))
        for j in range(0,k):
            s=int(random.randint(0,c-2))
            branches[i][s]=int(random.randint(0,AllF-1))
    return branches

# Compare modified candidate solutions with their previous states and keep changes that improve fitness
def CheckImprovments(branches,BR):
    r=len(branches)
    c=len(branches[0])-1
    for i in range(0,r):
        if ((BR[i][c]<branches[i][c])|(branches[i][c]==0))&(BR[i][c]>0):
            branches[i]=BR[i]
    return branches

# Getting the minimum fitness value
def GetMin(branches):
    c=len(branches[0])-1
    mi=branches[0][c]
    for i in range(1,len(branches)):
        if branches[i][c]<mi:
            mi=branches[i][c]
    return mi

# In case of unsuccessful termination, this function recovers the latest state of the candidate solutions 
def ReadCSs(nob,F,NOF,CR):
    branches=np.zeros([nob,NOF+3])
    F=open('SF/TR_SF_'+str(EXCN)+'_'+str(CR)+'_'+DSN+'.txt','r')
    l=F.readlines()
    for i in range(0,nob):
        s=l[i].replace('\n','').split(',')
        for j in range(0,len(s)):
            if j<NOF+2:
                branches[i,j]=round(float(s[j]))
            else:
                branches[i,j]=float(s[j])
    F.close()
    return branches

# Implementation of the Trader algorithm to create a candidate feature subset.
# To run this algorithm, use the following command:
# python Trader.py RunNumber DatasetName
# If this is the first run, set RunNumber to 1.

from sklearn import svm
import numpy as np
import random
import multiprocessing as mp
import threading
#import matplotlib.pyplot as plt
import copy
from multiprocessing import set_start_method
import os
from math import *
import sys
EXCN=sys.argv[1]
DSN=sys.argv[2]
global branches,TRDT,TEDT,TRDL,TEDL
TRDT,TEDT,TRDL,TEDL=GetData(DSN)
nob=100
NOF=50
CR=0
noi=50
for i in range(1,noi+1):
    if os.path.exists('SF/TR_SF_'+str(EXCN)+'_'+str(i)+'_'+DSN+'.txt'):
        CR=i
if CR>0:
    branches=ReadCSs(nob,len(TRDT[0]),NOF,CR)
else:
    CR=0
    branches=initial(nob,len(TRDT[0]),NOF)
    branches=profit(branches)
ham=[]
nog=10
for i in range(CR+1,noi):
    branches=grouping(branches,nog)
    BR=copy.deepcopy(branches)
    BR=distributing(BR)
    BR=profit(BR)
    branches=CheckImprovments(branches,BR)
    BR=copy.deepcopy(branches)
    BR=retailing(BR,i,len(TRDT[0]),noi)
    BR=profit(BR)
    branches=CheckImprovments(branches,BR)
    V=GetMin(branches)
    ham.append(V)
    print(i,V)
    F=open('SF/Convergence_TR_'+str(EXCN)+'_'+DSN+'.txt','a')
    F.write(str(i)+','+str(V)+"\n")
    F.close()
    F=open('SF/TR_SF_'+str(EXCN)+'_'+str(i)+'_'+DSN+'.txt','w')
    fi=len(branches[0])
    for i in range(0,len(branches)):
        for j in range(0,fi-1):
            F.write(str(branches[i][j])+",")
        F.write(str(branches[i][fi-1])+'\n')

    F.close()
