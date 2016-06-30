import sys
import random

lines = []
fi = open(sys.argv[1],'r')
for line in fi:
    lines.append(line)
fi.close()

random.shuffle(lines)

fo = open(sys.argv[2],'w')
for item in lines:
    fo.write(item)
fo.close()

