#advs="1458 2259 2261 2821 2997 3358 3386 3427 3476 all"
advs="3476"
hdfsfolder=hdfs://172.16.7.12:9000/user/chensqi/ipinyoudata
localfolder=make-ipinyou-data

#trainData=train.yzx.txt
trainData=train.svm.txt.nds
testData=test.yzx.txt
outF=./output/output.mllib.nds.1.5
ratioFile=train.nds.ratio
#program=lryzx-spark.py
program=lr-spark-mllib.py

for adv in $advs; do
    echo $adv
    echo $program
    echo $outF
    rm $outF.$adv
    ~/spark-1.6.1-bin-hadoop2.6/bin/spark-submit --executor-memory 6G  --master spark://172.16.7.12:7077 $program $hdfsfolder/$adv/$trainData $localfolder/$adv/$testData $outF.$adv $localfolder/$adv/$ratioFile
done
