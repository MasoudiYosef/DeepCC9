def GetF(seq):
    ls=[]
    for i in range(0,140):
        if seq[i:i+4]=='AAAA':
            ls.append(i)
    c=0
    for i in range(0,len(ls)):
        for j in range(i+1,len(ls)):
            if (abs(ls[i]-ls[j])%10==0)|(abs(ls[i]-ls[j])%11==0)|(abs(ls[i]-ls[j])%12==0):
                c=c+1
    ls=[]
    for i in range(0,140):
        if seq[i:i+4]=='CGCG':
            ls.append(i)
    c1=len(ls)
    return [c,c1]
    
def FeatureExtract(PTR,REF,dis):
    from statistics import stdev
    P=len(PTR)
    R=len(REF)
    ls=[]
    for i in range(0,R-P+1):
        if REF[i:i+P]==PTR:
            ls.append(abs(i-dis))
    if len(ls)==0:
        STD,TN,AVG,FLG10=-1,-1,-1,-1
    else:
        TN=len(ls)
        AVG=((sum(ls))/(len(ls)))
        STD=0
        FLG10=0
        for i in range(0,len(ls)):
            for j in range(i+1,len(ls)):
                D=abs(ls[j]-ls[i])
                if (D%10==0)|(D%11==0)|(D%12==0):
                    FLG10=FLG10+1
        if TN>1:
            STD=stdev(ls)
    return [TN,AVG,STD,FLG10,FLG10,FLG10]

def PositionFeatures(PTR,REF,dis,PT):
    P=len(PTR)
    R=len(REF)
    for i in range(0,141):
        if i<=70:
            if REF[i:i+P]==PTR:
                PT[70-i]=1
        else:
            if REF[i:i+P]==PTR:
                PT[i-70]=1
    return PT

def FeatureExtractL(PTR,REF,dis):
    from statistics import stdev
    P=len(PTR)
    R=len(REF)
    ls=[]
    for i in range(0,22):
        if REF[i:i+P]==PTR:
            ls.append(abs(i-dis))
    for i in range(178,200):
        if REF[i:i+P]==PTR:
            ls.append(abs(i-dis))
    if len(ls)==0:
        STD,TN,AVG,FLG10=-1,-1,-1,-1
    else:
        TN=len(ls)
        AVG=((sum(ls))/(len(ls)))
        STD=0
        FLG10=0
        FLG11=0
        FLG12=0
        for i in range(0,len(ls)):
            for j in range(i+1,len(ls)):
                D=abs(ls[j]-ls[i])
                if (D%10==0)|(D%11==0)|(D%12==0):
                    FLG10=FLG10+1
        if TN>1:
            STD=stdev(ls)    
    return [TN,AVG,STD,FLG10,FLG10,FLG10]

def PositionFeaturesL(PTR,REF,dis,PT):
    P=len(PTR)
    R=len(REF)
    for i in range(0,22):
        if REF[i:i+P]==PTR:
            PT[i]=1
    for i in range(178,200):
        if REF[i:i+P]==PTR:
            PT[199-i]=1
    return PT