# Structure of a deep residual block
def basic_block(x, filters, stride=1):
    res = Conv1D(filters, kernel_size=8, strides=stride, padding='same')(x)
    res = BatchNormalization()(res)
    res = Activation('sigmoid')(res)
    res = Conv1D(filters, kernel_size=4, strides=1, padding='same')(res)
    res = BatchNormalization()(res)
    if stride != 1 or x.shape[-1] != filters:
        x = Conv1D(filters, kernel_size=4, strides=stride, padding='same')(x)
        x = BatchNormalization()(x)
    out = Add()([res, x])
    out = Activation('sigmoid')(out)
    return out

# Building the ResNet model
def build_resnet(input_shape):
    inputs = Input(shape=input_shape)
    x = Conv1D(128, kernel_size=16, strides=1, padding='same')(inputs)
    x = BatchNormalization()(x)
    x = Activation('sigmoid')(x)
    x = basic_block(x, filters=32)
    x = basic_block(x, filters=32)
    x = basic_block(x, filters=64, stride=4)
    x = basic_block(x, filters=64)
    x = basic_block(x, filters=64, stride=4)
    x = basic_block(x, filters=64)
    x = GlobalAveragePooling1D()(x)
    outputs = Dense(1, activation='sigmoid')(x)
    model = Model(inputs=inputs, outputs=outputs)
    return model

#Dividing data into train and test sets
def Prepare_Data():
    global DS
    F=open(DS+'.txt','r')
    DT=F.readlines()
    F.close()
    TRDT=[]
    TEDT=[]
    TRDL=[]
    TEDL=[]
    s=DT[0].split(',')
    el=len(s)
    for i in range(0,len(DT)):
        k=DT[i].replace('\n','').split(',')
        if len(k)!=el:
            continue
        l1=[]
        for r in range(0,len(k)-1):
            l1.append(float(k[r]))
        if i%5!=0:
            TRDT.append(l1)
            TRDL.append(float(k[-1]))
        else:
            TEDT.append(l1)
            TEDL.append(float(k[-1]))
    R1=len(TRDT)
    R2=len(TEDT)
    C1=len(TRDT[0])
    C2=len(TEDT[0])
    TRDT=np.array(TRDT)
    TEDT=np.array(TEDT)
    TRDL=np.array(TRDL)
    TEDL=np.array(TEDL)
    TRDT=TRDT.reshape((R1,1,C1,1))
    TEDT=TEDT.reshape((R2,1,C2,1))
    return TRDT,TEDT,TRDL,TEDL,R1,R2,C1,C2

# Build the prediction model. To run it, use the following command:
# python ResNet.py DatasetName
from keras.models import Model
from keras.layers import Input, Conv1D, BatchNormalization, Activation, Add, GlobalAveragePooling1D, Dense
import numpy as np
import copy
import os
import sys
global DS
DS=sys.argv[1]
IN=int(sys.argv[2])
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
for it in range(IN,IN+1):
    TRDT,TEDT,TRDL,TEDL,R1,R2,C1,C2=Prepare_Data()
    input_shape = (1,C1)
    model = build_resnet(input_shape)
    model.summary()
    model.compile(loss='mean_squared_error',optimizer='adam',metrics=['mean_squared_error'])
    ne=500
    model.fit(TRDT,TRDL,epochs=1,batch_size=10,validation_data=(TEDT, TEDL),verbose=1)
    M1 = model.get_weights()
    res=model.evaluate(TEDT,TEDL,verbose=0)
    p=0
    OPT=['sgd','rmsprop','adam','adadelta','adagrad','adamax','nadam','ftrl']
    for epoch in range(ne):
        model.fit(TRDT,TRDL,epochs=1,batch_size=5,validation_data=(TEDT, TEDL),verbose=1)
        re=model.evaluate(TEDT,TEDL,verbose=0)
        if (res[1]>re[1]):
            p=0
            print('Improvment',epoch,re[1])
            res=copy.copy(re)
            M1=model.get_weights()
            F=open('PRE_'+DS+'_'+str(it)+'.txt','w')
            PRE=model.predict(TEDT)
            for i in range(0,len(TEDT)):
                F.write(str(i)+','+str(PRE[i])+','+str(TEDL[i])+'\n')
            PRE=model.predict(TRDT)
            for i in range(0,len(TRDT)):
                F.write(str(i)+','+str(PRE[i])+','+str(TRDL[i])+'\n')
            F.close()
        elif p>3:
            k=np.random.randint(len(OPT))
            model.compile(loss='mean_squared_error',optimizer=OPT[k],metrics=['mean_squared_error'])
            model.set_weights(M1)
        p=p+1
