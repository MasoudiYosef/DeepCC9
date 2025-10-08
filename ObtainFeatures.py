def ComSeq(seq):
    s=''
    seq=seq[::-1]
    for i in range(0,len(seq)):
        if seq[i]=='A':
            s=s+'T'
        if seq[i]=='T':
            s=s+'A'
        if seq[i]=='C':
            s=s+'G'
        if seq[i]=='G':
            s=s+'C'
    return s


def SimilarityScore(F,REF1,REF2):
    RE=LCS(REF1,REF2[::-1])
    F=[RE]
    RE=LCS(REF1,ComSeq(REF2))
    F.append(RE)
    return F


def CallFunc(PTR,REF,IDN,PO,dis):
    F=FeatureExtract(PTR,REF,dis)
    PO=PositionFeatures(PTR,REF,IDN,PO)
    return F,PO

def CallFuncL(PTR,REF,IDN,PO,dis):
    F=FeatureExtractL(PTR,REF,dis)
    PO=PositionFeaturesL(PTR,REF,IDN,PO)
    return F,PO


def WriteFeatures(F):
    s=''
    global Fe
    for j in range(0,len(F)):
        s=s+str(F[j])+','
    Fe.write(s)


import sys
from LCS import LCS
from FeatureExtract import FeatureExtract
from FeatureExtract import PositionFeatures
from FeatureExtract import FeatureExtractL
from FeatureExtract import PositionFeaturesL
from FeatureExtract import GetF
Arg1=sys.argv[1]
D=open(Arg1+'.txt','r')
DT=D.readlines()
D.close()
global Fe
Fe=open('Features'+Arg1,'w')
P=['A','T','C','G']
for i in range(0,len(DT)):
    PV=0
    print(i)
    dyad=100
    REF=DT[i][dyad-70:dyad+73]
    for a in P:
        for b in P:
            DI=[]
            for s in range(0,71):
                DI.append(0)
            PV=PV+1
            F,DI=CallFunc(a+b,REF,70,DI,70)
            WriteFeatures(F)
            WriteFeatures(DI)
            for c in P:
                TI=[]
                for s in range(0,71):
                    TI.append(0)
                PV=PV+1
                F,TI=CallFunc(a+b+c,REF,70,TI,70)
                WriteFeatures(F)
                WriteFeatures(TI)
    #F=GetF(REF)
    #WriteFeatures(F)
    F=[]
    F=SimilarityScore(F,REF[0:70],REF[71:141])
    WriteFeatures(F) 
    REF=DT[i][dyad-100:dyad+103]
    DI=[]
    TI=[]
    PV=0
    for a in P:
        for b in P:
            DI=[]
            for s in range(0,22):
                DI.append(0)
            PV=PV+1
            F,DI=CallFuncL(a+b,REF,100,DI,100)
            WriteFeatures(F)
            WriteFeatures(DI)
            for c in P:
                TI=[]
                for s in range(0,22):
                    TI.append(0)
                PV=PV+1
                F,TI=CallFuncL(a+b+c,REF,PV,TI,100)
                WriteFeatures(F)
                WriteFeatures(TI)
    F=[]
    F=SimilarityScore(F,REF[0:22],REF[178:200])
    WriteFeatures(F)
    if Arg1=='TP':
        Fe.write('1\n')
    else:
        Fe.write('0\n')
Fe.close()