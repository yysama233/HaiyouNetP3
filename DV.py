
from string import *
import sys
from collections import defaultdict
from copy import deepcopy

class Router(object):
    def __init__(self,num):
        self.num = num
        self.AdjList = []
        self.interation = 0
        self.costList = {self.num:0}
        self.destTable = {}
    #def getDist(self,dest):
    #    return self.destRoutes[dest]
    #def addRoute(self,dest,dist):
    #    self.destRoutes[dest]=dist
    def addAdj(self,dest,cost):
        self.AdjList.append(dest)
        self.costList[dest]=cost

    def addAdj(self,dest,cost):
        if (dest not in self.AdjList):
            self.AdjList.append(dest)
        self.updateCost(dest,cost)
    def rmAdj(self, dest):
        self.AdjList = [x for x in self.AdjList if x != dest]
        self.updateCost(dest,float('inf'))

    def updateCost(self,dest,cost):
        self.costList[dest] = cost
    def iniDestTable(self,numOfRouters):
        for i in range (1,numOfRouters+1):
            if i == self.num:
                #print "ini self"
                self.destTable[i] = [self.num,0,0]
                #print self.destTable[i]
            elif i in self.AdjList:
                #print "ini adj"
                self.destTable[i] = [i,self.costList[i],1]
                #print self.destTable[i]
            else:
                #print "unknown"
                self.destTable[i] = [-1,float('inf'),-1]

                #print self.destTable[i]
            #print "finish dest ini\n"
    def toString(self,numOfRouters):
        out = "%d\t"%self.num
        for i in range(1,numOfRouters+1):
            out += "%d,%d \t"%(self.destTable[i][0],self.destTable[i][2])
        out += "\n"
        return out
    def updateDest(self,dest,nextHop,distance,numHops):
        self.destTable[dest] = [nextHop,distance,numHops]

# The method to initialize all routers in the network
def iniRouter(routerFile):
    try:
        RouteF = open(routerFile,'r')
    except:
        print("Invalid file")
        sys.exit()
    netWork ={}
    ttlRNum = int(RouteF.readline())
    print "total Number of router", ttlRNum
    for i in range(1, ttlRNum + 1):
        tempR = Router(i)
        netWork[i] = tempR
    l =  RouteF.readline()
    while l:
        #print l
        r1,r2,cost = l.split()
        netWork[int(r1)].addAdj(int(r2),int(cost))
        netWork[int(r2)].addAdj(int(r1),int(cost))
        l =  RouteF.readline()

    #print "add cost finished"

    for i in range(1,ttlRNum + 1):
        #print "ini router destance",i
        netWork[i].iniDestTable(ttlRNum)
    return netWork

def iniEvent(eventFile):
    eventlist = []
    roundlist = []
    try:
        eventF = open(eventFile,'r')
    except:
        print("Invalid event file")
        sys.exit()
    l = eventF.readline()
    while l:
        rNum,r1,r2,newCost = l.split()
        eventDetails = [int(rNum), int(r1), int(r2), int(newCost)]
        eventlist.append(eventDetails)
        roundlist.append(int(rNum))
        l = eventF.readline()

    if (len(roundlist)>0):
        final_event = max(roundlist)
    else:
        final_event = -1
    return eventlist,roundlist,final_event


# calculateDV method to calculate a single source routers distance vectors
def calculateDV(oldnetWork, netWork,srcRouter, poison=False, split=False):
    Overallchanged = False
    for destNum,destRouter in netWork.items():
        if destNum == srcRouter.num:
            continue
        nextHop,minCost,numHops = srcRouter.destTable[destNum]
        tempCost = float('inf')

        # check all neighbours if they can reach destination
        for adjNum in srcRouter.AdjList:
            #print "new network:", netWork[adjNum].destTable[destNum], "old network: ", oldnetWork[adjNum].destTable[destNum]
            #print netWork[adjNum].destTable[destNum] == oldnetWork[adjNum].destTable[destNum]
            adjCost = srcRouter.costList[adjNum]
            adjDest = oldnetWork[adjNum].destTable[destNum][1]
            adjNexthop = oldnetWork[adjNum].destTable[destNum][0]
            adjNumHops = oldnetWork[adjNum].destTable[destNum][2]
            #print "adjNextHop:", adjNexthop, "src:", srcRouter.num
            if oldnetWork[adjNum].destTable[destNum][0] == srcRouter.num:
                if poison:
                    print "poison (sending infinity as distance)!", "src:", srcRouter.num, "nexthop:", adjNum,"dest:", destNum, "new distance:", adjDest + adjCost, "num hops:", adjNumHops+1
                    adjDest = float('inf')
                elif split:
                    print "split(not sending distance vector)!", "src:", srcRouter.num, "nexthop:", adjNum,"dest:", destNum, "new distance:", adjDest + adjCost, "num hops:", adjNumHops+1
                    # if split just don't send anything to that router
                    continue
                else:
                    #basic protocol
                    pass

            disFromAdj = adjDest + adjCost

            # finding the minimum among all dv from src to dest through different hops
            if disFromAdj < tempCost:
                tempCost = disFromAdj
                nextHop = adjNum
                numHops = adjNumHops+1

        if tempCost != minCost:
            print "update!", "src:", srcRouter.num, "nexthop:", nextHop,"dest:", destNum, "new distance:", tempCost,"num hops:", numHops 
            Overallchanged = True
            srcRouter.updateDest(destNum,nextHop,tempCost,numHops)

        if tempCost > 100:
            print "Count to infinity problem! End iteration."
            sys.exit()

    return Overallchanged

# choosing a routing protocol
# default is not recalculate and is basic protocol
def routingProtocol(netWork, numIterations, basicF, flag,poison=False, split=False):
    #basic if poison == false and split == false
    Overallchanged = False
    if not (poison or split):
        print "basic protocol"
    elif(poison):
        print "poison reversed protocol"
    else:
        print "split horizon protocol"
    if flag == 1:
        printNet(netWork,numIterations,basicF)

    # iteration all source router
    print "--------------------------protocol start--------------------------"
    oldnetWork = deepcopy(netWork)
    for srcNum,srcRouter in netWork.items():
        # check distance vector for every destination
        localChanged = calculateDV(oldnetWork,netWork,srcRouter,poison=poison,split=split)
        if localChanged:
            Overallchanged = True
    print "--------------------------protocol end----------------------------"
    return Overallchanged

def printNet(network,numIter,outFile):
    outFile.write("Round: %d\n"%numIter)
    print ("Round: %d"%numIter)
    for idx,router in network.items():
        outFile.write(router.toString(len(network)))
        print (router.toString(len(network)))

def printDelay(outFile, delay, protocol):
    out = "Convergence Delay:%d"%delay
    outFile.write(out)
    print protocol + ": " + out

def increaseEventDelay(basicChange, splitChange, poisonChange ,eventDelay):
    if len(eventDelay) == 0:
        return;
    else:
        if basicChange:
            eventDelay['basic'] += 1
        if splitChange:
            eventDelay['split'] += 1
        if poisonChange:
            eventDelay['poison'] += 1
    return eventDelay

def programStart(argv):
    if (len(argv)!=4):
        print("Invalid arguments")
        sys.exit()
    routerFile = argv[1]
    netWorkbasic = iniRouter(routerFile)
    if not netWorkbasic:
        print("invalid router file")
        sys.exit()
    netWorksplit = deepcopy(netWorkbasic)
    netWorkpoison = deepcopy(netWorkbasic)
    eventFile = argv[2]
    eventlist,roundlist, max_event = iniEvent(eventFile)

    flag = int(argv[3])
    if flag == 1:
        basicF = open("output-detailed-basic.txt",'w')
        splitF = open("output-detailed-split-horizon.txt",'w')
        reverse = open("output-detailed-poison-reversed.txt",'w')
    else:
        basicF = open("output-basic.txt",'w')
        splitF = open("output-split-horizon.txt",'w')
        reverse = open("output-poison-reversed.txt",'w')

#start of the first ALGORITHM

    # initialize all useful values
    numIterations = 0
    converged = False
    eventlist_counter = 0
    eventDelay={}
    OverallchangedBasic = True
    OverallchangedSplit = True
    OverallchangedPoison = True

    while not converged or numIterations <= max_event:
        event_trigger = False
        if (numIterations in roundlist):
            # if event triggered, we only do cost updates and r1,r2 dv updates
            roundNum = eventlist[eventlist_counter][0]
            r1 = eventlist[eventlist_counter][1]
            r2 = eventlist[eventlist_counter][2]
            newCost = eventlist[eventlist_counter][3]
            if newCost != -1:
                netWorkbasic[r1].addAdj(r2,newCost)
                netWorkbasic[r2].addAdj(r1,newCost)
                netWorksplit[r1].addAdj(r2,newCost)
                netWorksplit[r2].addAdj(r1,newCost)
                netWorkpoison[r1].addAdj(r2,newCost)
                netWorkpoison[r2].addAdj(r1,newCost)
            else:
                netWorkbasic[r1].rmAdj(r2)
                netWorkbasic[r2].rmAdj(r1)
                netWorksplit[r1].rmAdj(r2)
                netWorksplit[r2].rmAdj(r1)
                netWorkpoison[r1].rmAdj(r2)
                netWorkpoison[r2].rmAdj(r1)
            print "event:", "router1:", r1,"router2:", r2,"newcost:", newCost
            eventlist_counter+=1
            event_trigger = True

            # initialize eventDelay with value = 0
            eventDelay['basic'] = 0
            eventDelay['split'] = 0
            eventDelay['poison'] = 0

            OverallchangedBasic = True
            OverallchangedSplit = True
            OverallchangedPoison = True
            converged = False

            # recalculate dv for r1 and r2
            print "------------------------round ", numIterations," recalculate---------------------"
            calculateDV(deepcopy(netWorkbasic),netWorkbasic,netWorkbasic[r1])
            calculateDV(deepcopy(netWorkbasic),netWorkbasic,netWorkbasic[r2])
            calculateDV(deepcopy(netWorksplit),netWorksplit,netWorksplit[r1], split=True)
            calculateDV(deepcopy(netWorksplit),netWorksplit,netWorksplit[r2], split=True)
            calculateDV(deepcopy(netWorkpoison),netWorkpoison,netWorkpoison[r1], poison=True)
            calculateDV(deepcopy(netWorkpoison),netWorkpoison,netWorkpoison[r2], poison=True)
            print "--------------------------finish recalculation--------------------"
        else:
            # if not event trigger we are normally doing routing protocols
            OverallchangedBasic = routingProtocol(netWorkbasic, numIterations, basicF, flag)
            OverallchangedSplit = routingProtocol(netWorksplit, numIterations, splitF, flag,split=True)
            OverallchangedPoison = routingProtocol(netWorkpoison, numIterations, reverse, flag, poison=True)
            print "overall changed basic: ", OverallchangedBasic
            print "overall changed split: ", OverallchangedSplit
            print "overall changed poison: ", OverallchangedPoison
            print "------------------------round ", numIterations, " finished------------------------" 
            if not (OverallchangedBasic or OverallchangedPoison or OverallchangedSplit):
                converged = True

        numIterations += 1
        # if there are any value in event delay, we increase the iteration number in event delay
        increaseEventDelay(OverallchangedBasic,OverallchangedPoison,OverallchangedSplit,eventDelay)


    if flag==0:
        printNet(netWorkbasic,numIterations-1,basicF)
        printNet(netWorksplit,numIterations-1,splitF)
        printNet(netWorkpoison,numIterations-1,reverse)
    for protocol,delay in eventDelay.items():
        if protocol == "basic":
            printDelay(basicF,delay, protocol)
        elif protocol == "poison":
            printDelay(reverse, delay, protocol)
        else:
            printDelay(splitF, delay, protocol) 
    basicF.close()
    splitF.close()
    reverse.close()

if __name__ == "__main__":
    programStart(sys.argv)
