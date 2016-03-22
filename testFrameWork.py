#!/usr/bin/python
import sys
import random

random.seed(10)

def biddingFunction_const(bid):
    return bid

def biddingFunction_rand(upper):
    return int(random.random() * upper)

def biddingFunction_mcpc(ecpc, pctr):
    return int(ecpc * pctr)

def biddingFunction_lin(pctr, basectr, basebid):
    return int(pctr *  basebid / basectr)

def biddingFunction_win(ccfme, bid):
    return bid >= ccfme[2] and bid > ccfme[3]

def win(bidRequest, bid):
    return bid > int(bidRequest[1])

# Run one bid
# Return (imp, clk, cnv, cost)
def RTB(budget, traindataFileName, traindataModel, bidRequest, biddingStrategy):
    bid = 0
    if biddingStrategy["name"] == "const":
        bid = biddingFunction_const( biddingStrategy["paras"] )
    #TODO and other strategies...
    else :
        print 'Unknow strategy'

    if win(bidRequest, bid):
        return (1,int(bidRequest[0]),int(bidRequest[0]),int(bidRequest[1]))
    else:
        return (0,0,0,0)

# Run test environment for testdatas
# Return (imps, clks, cnvs and costs)
def testEnv(budget, traindataFileName, traindataModel, testdataFileName, biddingStrategy):
    # read in test data
    fi = open(testdataFileName, 'r')
    first = True
    imps = 0
    clks = 0
    cnvs = 0
    costs = 0
    for line in fi:
        s = line.split(' ')
        if first:
            first = False
            continue
        (imp, clk, cnv, cost) = RTB(budget, traindataFileName, traindataModel, s, biddingStrategy)
        budget = budget - cost
        imps += imp
        clks += clk
        cnvs += cnv
        costs += cost

        #clk = int(s[27])
        #cnv = int(s[28])
        #floorprice = int(s[20])
        #marketprice = int(s[23])
        #ccfm.append((clk, cnv, floorprice, marketprice))
        #totalcost+= marketprice
    fi.close()
    return (imps,clks,cnvs,costs)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print 'Usage: budget train.log.txt test.log.txt. NameOfStrategy \n\n For instance\n ./testFrameWork 1000 **.txt **.txt const \n'
        exit(-1)
        
    budget = int(sys.argv[1])
    traindataFileName = sys.argv[2]
    testdataFileName = sys.argv[3]

    # -------------------- Important parameters for construct bidding strategy ---------------------
    constParas = 10000
    randParas = random.randint(1,100)
    strategyParas = {"const":constParas,"rand":randParas}
    # --------------------------------------------------------

    biddingStrategy = {"name":sys.argv[4], "paras":strategyParas[ sys.argv[4] ] }
    if ( biddingStrategy["paras"] != None ):
        imps = 0
        clks = 0
        cnvs = 0
        costs = 0
        (imps, clks, cnvs, costs) = testEnv(budget,traindataFileName,"Null",testdataFileName,biddingStrategy)
        print 'imps:' + str(imps)
    else:
        print 'Bidding strategy does not exist!'
