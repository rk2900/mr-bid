import sys

def turnToSVMFile(inputFile,outputFile):
    fi = open(inputFile,'r')
    fo = open(outputFile,'w')
#    fo = NamedTemporaryFile(delete=True)
    for line in fi:
        t = line.split()
        fo.write(t[0])
        dict = {}
        for item in t[2:]:
            dict[ int(item.split(':')[0]) ] = int(item.split(':')[1])
            #fo.write(' ')
            #fo.write(item)
        for a,b in sorted(dict.items()) :
            fo.write(' ')
            fo.write(str(a+1))
            fo.write(':')
            fo.write(str(b))
        fo.write('\n')
#    fo.flush()
    fi.close()
    fo.close()
#    return fo

turnToSVMFile(sys.argv[1],sys.argv[2])
