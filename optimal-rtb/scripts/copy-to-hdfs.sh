#advs="2261"
$advs="2261 1458 2259 2821 2997 3358 3386 3427 3476 all"
advs="all"
folder=../../make-ipinyou-data
file=train.yzx.txt
for adv in $advs; do
    echo $adv
    #python ../python/makeSVMFile.py $folder/$adv/train.yzx.txt $folder/$adv/train.svm.txt
    /usr/local/hadoop/bin/hadoop fs -mkdir /user/chensqi/ipinyoudata/$adv/
    /usr/local/hadoop/bin/hadoop fs -rm /user/chensqi/ipinyoudata/$adv/$file
    /usr/local/hadoop/bin/hadoop fs -put $folder/$adv/$file /user/chensqi/ipinyoudata/$adv
done
