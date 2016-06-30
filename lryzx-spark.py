#!/usr/bin/python
import sys
import random
import math
import operator
from sklearn.metrics import roc_auc_score
from sklearn.metrics import mean_squared_error

from pyspark import SparkContext
from operator import add
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.regression import SparseVector 
from pyspark.mllib.classification import LogisticRegressionWithSGD
from pyspark.mllib.classification import LogisticRegressionWithLBFGS
from pyspark.mllib.util import MLUtils

import time


bufferCaseNum = 1000000
eta = 0.01
lamb = 1E-6
featWeight = {}
trainRounds = 10
random.seed(10)
initWeight = 0.05

def nextInitWeight():
    return (random.random() - 0.5) * initWeight

def ints(s):
    res = []
    for ss in s:
        res.append(int(ss))
    return res

def sigmoid(p):
    if p < -10:
        return 0
    if p > 10:
        return 1
    return 1.0 / (1.0 + math.exp(-p))


if len(sys.argv) < 4:
    print 'Usage: train.yzx.txt test.yzx.txt result.txt'
    exit(-1)

beginTime = time.time()

sc = SparkContext(appName="myDistributedLR")
textFile = sc.textFile(sys.argv[1])

n = textFile.count()
for round in range(0, trainRounds):
    # train for this round
    print 'round# ' + str(round)
    
    sc.broadcast(featWeight)
    def seqOp(featweight,data):
        data = ints(data.replace(":1", "").split())
        clk=data[0]
        mp=data[1]
        fsid=2
        pred=0.0
        for i in xrange(fsid,len(data)):
            feat = data[i]
            if feat not in featWeight:
                featWeight[feat] = nextInitWeight()
            pred += featWeight[feat]
        pred = sigmoid(pred)
        
        for i in xrange(fsid,len(data)):
            feat = data[i]
            featWeight[feat] = featWeight[feat]*(1-lamb) + (clk-pred)*eta
        return featWeight
    def combOp(weight1,weight2):
        for k,v in weight2.items():
            if k not in weight1:
                weight1[k] = 0.0
            weight1[k] = weight1[k] + v
        return weight1
    # train a round
    featWeight = textFile.treeAggregate(featWeight,seqOp,combOp)
    for k,v in featWeight.items():
        featWeight[k] /= 2
    

    
y = []
yp = []
with open(sys.argv[2], 'r') as fi:
    for line in fi:
        data = ints(line.replace(":1", "").split())
        clk = data[0]
        mp = data[1]
        fsid = 2 # feature start id
        pred = 0.0
        for i in range(fsid, len(data)):
            feat = data[i]
            if feat in featWeight:
                pred += featWeight[feat]
        pred = sigmoid(pred)
        y.append(clk)
        yp.append(pred)
    fi.close()
auc = roc_auc_score(y, yp)
rmse = math.sqrt(mean_squared_error(y, yp))
def calc_cross_entropy(p,q):
    cnt = 0
    res = 0
    for pi,qi in zip(p,q):
        qi = sigmoid(qi)
        res += (-pi) * math.log(qi) - (1-pi)*math.log(1-qi)
        cnt += 1
    return res/cnt
cross_entropy = calc_cross_entropy(y,yp)
endTime = time.time()

with open(sys.argv[3],'w') as fo:
    fo.write('(auc,rmse,cross_entropy): ' + str(auc) + ',' + str(rmse) + ',' + str(cross_entropy))
    fo.write('\n')
    fo.write('time:i ' + str(endTime-beginTime) + " seconds")
sc.stop()


