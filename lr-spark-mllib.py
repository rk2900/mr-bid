from pyspark import SparkContext
from operator import add
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.regression import SparseVector 
from pyspark.mllib.classification import LogisticRegressionWithSGD
from pyspark.mllib.classification import LogisticRegressionWithLBFGS
from pyspark.mllib.util import MLUtils
from sklearn.metrics import roc_auc_score
from sklearn.metrics import mean_squared_error
from tempfile import NamedTemporaryFile

import sys
import math
import time

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


def turnToSVMFile(inputFile,outputFile):
    fi = open(inputFile,'r')
#    fo = open(outputFile,'w')
    fo = NamedTemporaryFile(delete=True)
    for line in fi:
        t = line.split()
        fo.write(t[0])
        for item in t[2:]:
            fo.write(' ')
            fo.write(item)
        fo.write('\n')
    fo.flush()
    fi.close()
    fo.close()
    return fo
def calc_cross_entropy(p,q):
    cnt = 0
    res = 0
    for pi,qi in zip(p,q):
        qi = sigmoid(qi)
        res += (-pi) * math.log(qi) - (1-pi)*math.log(1-qi)
        cnt += 1
    return res/cnt

if len(sys.argv) < 3:
    print 'Usage: train.svm.txt test.yzx.txt outputFile.txt ratioFile.txt'
    exit(-1)


beginTime = time.time()
sc = SparkContext(appName="testsparkLR")
vectorSize = 1000000

#tempFileName = 'SVMFile'

#turnToSVMFile( sys.argv[1], tempFileName ).name
#example = MLUtils.loadLibSVMFile( sc,  sys.argv[1]  )
numFeat = 1000000
example = MLUtils.loadLibSVMFile( sc,  sys.argv[1] , numFeatures = numFeat )

#print example[1]

print 'training begin!'
#lrm = LogisticRegressionWithSGD.train(sc.parallelize(data), iterations=10)
lrm = LogisticRegressionWithSGD.train( example , iterations=100)
print 'training finish!'

lrm.clearThreshold()

positive = 0.0
negative = 0.0
if ( len(sys.argv) > 4 ):
    with open(sys.argv[4]) as fooo:
        for line in fooo:
            positive = float(line.split(',')[0])
            negative = float(line.split(',')[1])

y = []
yp = []
with open(sys.argv[2]) as fi:
    for line in fi:
        datai = ints(line.replace(":1", "").split())
        clk = datai[0]
        mp = datai[1]
        fsid = 2 # feature start id
        thisdict = {}
        for i in range(fsid, len(datai)):
            feat = datai[i]
            thisdict[feat] = 1
        pred = lrm.predict(SparseVector(lrm.numFeatures,thisdict))
        y.append(clk)
        yp.append(pred)
    print type(yp[0])
    print type(y[0])
#fi.close()
auc = roc_auc_score(y, yp)

#if ( len(sys.argv) > 4 ):
#    def mapPredict(p):
#        return p/( p+ (1-p)*negative )
#    map(mapPredict,yp)
    
rmse = math.sqrt(mean_squared_error(y, yp))
cross_entropy = calc_cross_entropy(y,yp)


endTime = time.time()

with open(sys.argv[3],'w') as fo:
    fo.write('(auc,rmse,cross_entropy): ' + str(auc) + ',' + str(rmse) + ',' + str(cross_entropy))
    fo.write('\n')
    fo.write('time:i ' + str(endTime-beginTime) + " seconds")


#print lrm.predict(SparseVector(vectorSize,{1:1}))

sc.stop()
