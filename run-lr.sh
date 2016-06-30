#advs="2997 1458 2259 2261 2821 3358 3386 3427 3476"
#advs="2997 2821 3427 1458 all"
#advs="all"
advs="3427 1458"
hdfsfolder=hdfs://172.16.7.12:9000/user/chensqi/ipinyoudata
localfolder=make-ipinyou-data

#trainData=train.yzx.txt
trainData=train.svm.txt

testData=test.yzx.txt

outF=./output/output.mllib.trainround10

#program=lryzx-spark.py
#program=lr-spark-svm.py
program=lr-spark-mllib.py

for adv in $advs; do
    echo $outF.$adv
    rm $outF.$adv
    ~/spark-1.6.1-bin-hadoop2.6/bin/spark-submit --executor-memory 6G  --master spark://172.16.7.12:7077 $program $hdfsfolder/$adv/$trainData $localfolder/$adv/$testData $outF.$adv
done
