#advs="2261"
#advs="2261 1458 2259 2821 2997 3358 3386 3427 3476"
advs="all"
#advs="2261"
folder=../../make-ipinyou-data
for adv in $advs; do
    echo $adv
    python ../python/makeSVMFile.py $folder/$adv/train.yzx.txt $folder/$adv/train.svm.txt
done
