from pyspark import SparkFiles
from pyspark import SparkContext

sc = SparkContext(appName="testHDF")

sc.addFile("hdfs://172.16.7.12:9000/user/chensqi/f1")
def func(iterator):
   with open(SparkFiles.get("f1")) as testFile:
      fileVal = int(testFile.readline())
      return [x * fileVal for x in iterator]
print sc.parallelize([1, 2, 3, 4]).mapPartitions(func).collect()

