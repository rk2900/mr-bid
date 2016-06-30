import sys
import random
import math

negative = []
positive = []

fi = open(sys.argv[1],'r')
for line in fi:
    if ( line.startswith('0')):
        negative.append(line)
    else:
        positive.append(line)
fi.close()

random.shuffle(negative)
random.shuffle(positive)

ratioPositive = int(sys.argv[4])
ratioNegative = int(sys.argv[5])

x = min( len(negative)/ratioNegative, len(positive)/ratioPositive )

foo = open(sys.argv[3],'w')
foo.write( str(float(x)*ratioPositive/len(positive)) + ',' + str(float(x)*ratioNegative/len(negative)) )
foo.close()

fo = open(sys.argv[2],'w')

outputList = []

index = 0
for item in positive:
    outputList.append(item)
    index+=1 
    if index >= x*ratioPositive:
        break

index=0
for item in negative:
    outputList.append(item)
    index+=1
    if index >= x*ratioNegative:
        break

random.shuffle(outputList)
for item in outputList:
    fo.write(item)

fo.close()
