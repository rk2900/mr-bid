#!/usr/bin/python
#import sys
#import random
#import math
#import operator
#from sklearn.metrics import roc_auc_score
#from sklearn.metrics import mean_squared_error
#
#from operator import add
#from pyspark import SparkContext
#from pyspark import SparkFiles

#sc = SparkContext(appName="tt")

#f1 = sc.wholeTextFiles("hdfs://172.16.7.12:9000/user/chensqi/optimal-rtb/python")
#f2 = sc.parallelize( [ tuple(f1.collect())] )
#print( f2.count() )

#print( f1.collect() )

#f2 = f1.flatMap( lambda x:x.split(' '))
#print( f2.count() )
#print( f2.collect())


#f2 = sc.wholeTextFiles("hdfs://172.16.7.12:9000/ipinyou/README.md")
#print( f2.count() )

#fR = sc.union([f1.values(),f2.values()])
#print( fR.count() )
#print( fR.collect() )

#fc = fR.cartesian(sc.parallelize([1,2]))
#print( fc.count())

#sc.stop()

#hehe = [(1,2),(3,4)]

#with open ('result','w') as fout:
#    fout.write(str(hehe))
#fout.close()

from itertools import cycle

a = [1,2]
b = [2,3,4]

c = zip(cycle(a),b)
print c
