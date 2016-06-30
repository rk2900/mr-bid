advs="1458 2259 2261 2821 2997 3358 3386 3427 3476"
#advs="2261"
folder=../../make-ipinyou-data
for adv in $advs; do
    echo $adv
    echo 'shuffling'
    python ../python/shuffle.py $folder/$adv/train.yzx.txt $folder/$adv/train.yzx.txt.shuffled
    #python ../python/lryzx.py $folder/$adv/train.yzx.txt $folder/$adv/test.yzx.txt $folder/output/output.$adv
    echo 'lr training'
    python ../python/lryzx.py $folder/$adv/train.yzx.txt.shuffled $folder/$adv/test.yzx.txt $folder/output/output.shuffled.$adv
done
