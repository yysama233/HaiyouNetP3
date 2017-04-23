
from string import *
import sys
from collections import defaultdict
from copy import deepcopy
"""
Author: Yang Yang, Mingjun Xie, Yufeng Wang
Version 1.0

Code for Project 3
"""
class Router(object):
    def __init__(self,num):
        """Function to initialize a Router

        Args:
            num: number of the router

        Returns:
            null

        """
        self.num = num
        self.AdjList = []
        self.interation = 0
        self.costList = {self.num:0}
        self.destTable = {}

    def addAdj(self,dest,cost):
        """Function to add an adjacent to the router

        Args:
            dest: number of the adjacent router
            cost: cost to that router

        Returns:
            null

        """
        if (dest not in self.AdjList):
            self.AdjList.append(dest)
        self.updateCost(dest,cost)
    def rmAdj(self, dest):
        """Function to remove the adjacent

        Args:
            dest: number of the adjacent

        Returns:
            null

        """
        self.AdjList = [x for x in self.AdjList if x != dest]
        self.updateCost(dest,float('inf'))
        if self.destTable[dest][0] == dest:
            self.destTable[dest] = [-1,float('inf'),-1]

    def updateCost(self,dest,cost):
        """Function to update the cost to an adjacent

        Args:
            dest: number of the adjacent
            cost: new cost

        Returns:
            null

        """
        self.costList[dest] = cost

    def iniDestTable(self,numOfRouters):
        """Function to initialize the router table

        Args:
            numOfRouters: total number of all routers

        Returns:
            null

        """
        for i in range (1,numOfRouters+1):
            if i == self.num:
                self.destTable[i] = [self.num,0,0]
            elif i in self.AdjList:
                self.destTable[i] = [i,self.costList[i],1]
            else:
                self.destTable[i] = [-1,float('inf'),-1]
    def toString(self,numOfRouters):
        """Function to print the table of the router

        Args:
             numOfRouters: total number of all routers

        Returns:
            null

        """
        out = "%d\t"%self.num
        for i in range(1,numOfRouters+1):
            out += "%d,%d \t"%(self.destTable[i][0],self.destTable[i][2])
        out += "\n"
        return out
    def updateDest(self,dest,nextHop,distance,numHops):
        """Function to update the router table

        Args:
            dest: the number of the router to update
            nextHop: new nextHop
            distance:new distance
            numHops: new number of Hops

        Returns:
            null

        """
        self.destTable[dest] = [nextHop,distance,numHops]

# The method to initialize all routers in the network
def iniRouter(routerFile):
    """Function to initialze all Routers

        Args:
            routerFile: the router File

        Returns:
            network: the network of all routers

        """
    try:
        RouteF = open(routerFile,'r')
    except:
        print("Invalid file")
        sys.exit()
    netWork ={}
    ttlRNum = int(RouteF.readline())
    for i in range(1, ttlRNum + 1):
        tempR = Router(i)
        netWork[i] = tempR
    l =  RouteF.readline()
    while l:
        r1,r2,cost = l.split()
        netWork[int(r1)].addAdj(int(r2),int(cost))
        netWork[int(r2)].addAdj(int(r1),int(cost))
        l =  RouteF.readline()


    for i in range(1,ttlRNum + 1):
        netWork[i].iniDestTable(ttlRNum)
    return netWork

def iniEvent(eventFile):
    """Function the initialize all events

        Args:
            eventFile: eventFile

        Returns:
            eventlist: list of all events
            roundlist: list of all rounds which have event
            final_event: the round of the final event

        """
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
    """Function the calculate the distance vector

        Args:
            oldnetWork: the current network
            netWork: the network to be updated
            srcRouter:the surce router
            poison: if use poison algorithm
            split: if use split algorithm

        Returns:
            overallChanged: if the table changed
            infinity: if count to infinity happend in this round

        """
    Overallchanged = False
    infinity=False
    for destNum,destRouter in netWork.items():
        if destNum == srcRouter.num:
            continue
        nextHop,minCost,numHops = srcRouter.destTable[destNum]
        tempCost = float('inf')

        # check all neighbours if they can reach destination
        for adjNum in srcRouter.AdjList:

            adjCost = srcRouter.costList[adjNum]
            adjDest = oldnetWork[adjNum].destTable[destNum][1]
            adjNexthop = oldnetWork[adjNum].destTable[destNum][0]
            adjNumHops = oldnetWork[adjNum].destTable[destNum][2]
            if oldnetWork[adjNum].destTable[destNum][0] == srcRouter.num:
                if poison:
                    adjDest = float('inf')
                elif split:
                    continue
                else:
                    
                    pass

            disFromAdj = adjDest + adjCost

            # finding the minimum among all dv from src to dest through different hops
            if disFromAdj < tempCost:
                tempCost = disFromAdj
                nextHop = adjNum
                numHops = adjNumHops+1
        if tempCost == float('inf'):
            nextHop = -1
            numHops = -1
        if tempCost != minCost:
            Overallchanged = True
            srcRouter.updateDest(destNum,nextHop,tempCost,numHops)

        if numHops > 100:
            
            infinity = True
            Overallchanged = False
            return Overallchanged,infinity
            

    return Overallchanged,infinity

# choosing a routing protocol
# default is not recalculate and is basic protocol
def routingProtocol(netWork, numIterations, outF, flag,poison=False, split=False):
    """Function the calculate DV for all routers

        Args:
            netWork: the netWork to update
            numIterations: the round number
            outF: the file to print to
            flag: the print out mode
            poison: if use poison algorithm
            split: if use split algorithm

        Returns:
            overallChanged: if the table changed
            infinity: if count to infinity happend in this round

        """
    #basic if poison == false and split == false
    Overallchanged = False
    if flag == 1:
        printNet(netWork,numIterations,outF)

    # iteration all source router
    
    oldnetWork = deepcopy(netWork)
    for srcRouter in netWork.values():
        # check distance vector for every destination
        localChanged,infinity = calculateDV(oldnetWork,netWork,srcRouter,poison,split)
        if localChanged:
            Overallchanged = True
        if infinity:
            outF.write("Count to infinity problem! End iteration.\n")
            break

    return Overallchanged,infinity

def printNet(network,numIter,outFile,flag=1):
    """Function to print the table to the file

        Args:
            network:current network
            numIter: number of rounds
            outFile: the file to print to
            flag: the printing mode

        Returns:
            none

        """
    if flag:
        outFile.write("Round: %d\n"%numIter)
   
    for router in network.values():
        outFile.write(router.toString(len(network)))
  

def printDelay(outFile, delay, infinity):
    """Function to print convergence delay

        Args:
            outFile: the file to print to
            delay: convergence delay
            infinity: if count to infinity happened

        Returns:
            none

        """
    if infinity:
        outFile.write("Convergence Delay:N/A")
    else:
        outFile.write("Convergence Delay:%d"%delay)
   

def programStart(argv):
    """Function of the enter of the program, conduct three algorithms in sequence

        Args:
            argv: command input

        Returns:
            none

        """
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
        poisonF = open("output-detailed-poison-reversed.txt",'w')
        print ("output-detailed-basic.txt|output-detailed-split-horizon.txt|output-detailed-poison-reversed.txt")
    else:
        basicF = open("output-basic.txt",'w')
        splitF = open("output-split-horizon.txt",'w')
        poisonF = open("output-poison-reversed.txt",'w')
        print ("output-basic.txt|output-split-horizon.txt|output-poison-reversed.txt")
    mainLoop(basicF,netWorkbasic,eventlist,roundlist,max_event,flag)
    mainLoop(splitF,netWorksplit,eventlist,roundlist,max_event,flag,False,True)
    mainLoop(poisonF,netWorkpoison,eventlist,roundlist,max_event,flag,True,False)
    
    

def mainLoop(outF,netWork,eventlist,roundlist,max_event,flag,poison=False,split=False):
    """Function to calculate a specific algorithm

        Args:
            outF: the file to print to
            netWork: the network to calculate
            eventlist: list of events
            roundlist: list of event rounds
            max_event: the final event round
            flag: printing mode
            poison: if use poison alorithm
            split: if use split mode

        Returns:
            none

        """
    numIterations = 1
    converged = False
    eventlist_counter = 0
    eventDelay=0
    Overallchanged = True
    infinity = False
    while not converged or numIterations <= max_event:

        if (numIterations in roundlist):
            # if event triggered, we only do cost updates and r1,r2 dv updates
            roundNum = eventlist[eventlist_counter][0]
            r1 = eventlist[eventlist_counter][1]
            r2 = eventlist[eventlist_counter][2]
            newCost = eventlist[eventlist_counter][3]
            if newCost != -1:
                netWork[r1].addAdj(r2,newCost)
                netWork[r2].addAdj(r1,newCost)
            else:
                netWork[r1].rmAdj(r2)
                netWork[r2].rmAdj(r1)
           
            eventlist_counter+=1
           

            # initialize eventDelay with value = 0
            eventDelay = 0

            Overallchanged = True
            converged = False

            # recalculate dv for r1 and r2
           
            if flag == 1:
                printNet(netWork,numIterations,outF)
            calculateDV(deepcopy(netWork),netWork,netWork[r1],poison,split)
            calculateDV(deepcopy(netWork),netWork,netWork[r2],poison,split)
            
           
        else:
            # if not event trigger we are normally doing routing protocols
            Overallchanged,infinity = routingProtocol(netWork, numIterations, outF, flag,poison,split) 
        if not Overallchanged:
            converged = True
        else:
            eventDelay+= 1
        numIterations += 1
        if infinity:
            break
        # if there are any value in event delay, we increase the iteration number in event delay
        


    if flag == 0:
        printNet(netWork,numIterations-1,outF,flag)
    printDelay(outF,eventDelay,infinity)
    outF.close()

if __name__ == "__main__":
    programStart(sys.argv)