
from string import *
import sys
from collections import defaultdict
from copy import deepcopy

class DV:
    def __init__(self, src, dst, cost, next_hop, num_hops):
        self.src = src
        self.dst = dst
        self.cost = cost
        self.next_hop = next_hop
        self.num_hops = num_hops
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.src == other.src and self.dst == other.dst and self.cost == other.cost and
            self.next_hop == other.next_hop and self.num_hops == other.num_hops)
        return False
    #def to_string(self):
     #   print("(Distance vector", self.src, self.dst, self.cost, self.next_hop, self.num_hops, ")\t", end= '')

class Router(object):
    def __init__(self,num):
        self.num = num
        self.AdjList = []
        self.interation = 0
        self.updated = False
        self.costList = {}
        self.destTable = {}
    #def getDist(self,dest):
    #    return self.destRoutes[dest]
    #def addRoute(self,dest,dist):
    #    self.destRoutes[dest]=dist
    def addAdj(self,dest,cost):
        self.AdjList.append(dest)
        self.costList[dest]=cost
    def rmRoute(self,dest):
        del destRoutes[dest]
    def updateCost(self,dest,cost):
        self.costList[dest] = cost
    def iniDestTable(self,numOfRouters):
        for i in range (1,numOfRouters+1):
            if i == self.num:
                #print "ini self"
                self.destTable[i] = [0,0]
                #print self.destTable[i]
            elif i in self.AdjList:
                #print "ini adj"
                self.destTable[i] = [0,self.costList[i]]
                #print self.destTable[i]
            else:
                #print "unknown"
                self.destTable[i] = [-1,-1]
                #print self.destTable[i]
            #print "finish dest ini\n"
    def toString(self,numOfRouters):
        out = "%d "%self.num
        for i in range(1,numOfRouters+1):
            out += "%d,%d\t"%(self.destTable[i][0],self.destTable[i][1])
        return out
    def updateDest(self,dest,nextHop,distance):
        self.destTable[nextHop,dest]
    # def Initialize_router_table(self,number_of_routers):
    #     self.table = []
    #     for r in range(number_of_routers):
    #         self.table.append([])
    #         #the row of itself
    #         if(r == (self.num - 1)):
    #             for i in range(number_of_routers):
    #                 if (i==(self.num-1)):
    #                     self.table[r].append(DV(self.num, self,num, 0 , None, 0))
    #                 elif((i+1) in self.AdjList):
    #                     self.table[r].append(DV(self.num, (i+1), getDist(self.AdjList[i+1]), (i+1), 1))
    #                 else:
    #                     not_existing = DV(self.num, (i+1), None, None, None)
    #                     self.table[r].append(not_existing)
    #         else:
    #             for i in range(number_of_routers):
    #                 not_existing = DV(r+1, i+1, None, None,None)
    #                 self.table[r].append(not_existing)

    # def new_update_table(self, dv_list, iteration, old_cost = 0, flag = False):

    #     for dv in dv_list:
    #         self.table[dv.src - 1][dv.dst - 1] = dv

    #     for i in range(len(self.table[self.id - 1])):
    #         old_dv = self.table[self.id - 1][i]
    #         dv = self.table[self.id - 1][i]
    #         if (dv.dst != self.id):
    #             dv_min = None
    #             min_cost = None
    #             dv_min_set = False
    #             #pick the smallest path to the dst among all neighbors
    #             for adjlist in self.neighbors: 
    #                 if (dv_min_set == False and self.table[AdjList - 1][dv.dst - 1].cost is not None):
    #                     dv_min_set = True
    #                     dv_min = self.table[AdjList - 1][dv.dst - 1]
    #                     min_cost = self.table[AdjList - 1][dv.dst - 1].cost + self.adjList[adjlist]
    #                 elif (self.table[adjlist - 1][dv.dst - 1].cost is not None and
    #                     self.table[adjlist - 1][dv.dst - 1].cost + self.adjList[adjlist] < min_cost):
    #                     dv_min = self.table[adjlist - 1][dv.dst - 1]
    #                     min_cost = self.table[adjlist - 1][dv.dst - 1].cost + self.adjList[adjlist]

    #             if (not dv_min_set):
    #                 none_dv = DV(self.id, dv.dst, None, None, None)
    #                 self.table[self.num - 1][dv.dst - 1] = none_dv

    #             elif (dv.dst in self.adjList and self.adjList[dv.dst] < min_cost):
    #                 print("result")
    #                 to_string(dv_min)
    #                 print("")
    #                 src = self.id
    #                 dst = dv_min.dst
    #                 cost = self.adjList[dv.dst]
    #                 next_hop = dv.dst
    #                 num_hops = 1
    #                 self.table[self.num - 1][dv.dst - 1] = DV(src, dst, cost, next_hop, num_hops)
    #             else:
    #                 print("result, min cost", min_cost)
    #                 to_string(dv_min)
    #                 print("")
    #                 src = self.id
    #                 dst = dv_min.dst
    #                 cost = min_cost
    #                 next_hop = dv_min.src
    #                 num_hops = dv_min.num_hops + 1
    #                 self.table[self.num - 1][dv.dst - 1] = DV(src, dst, cost, next_hop, num_hops)
    #             if (old_dv == self.table[self.num - 1][dv.dst - 1]):

    #                 self.set_update(0, iteration)
    #             else:

    #                 self.set_update(1, iteration)

    #             if (min_cost > 100):
    #                 print("Convergence instability")
    #                 exit()


# The method to initialize all routers in the network
def iniRouter(routerFile):
    try:
        RouteF = open(routerFile,'r')
    except:
        print("Invalid file")
        sys.exit()
    netWork ={}
    ttlRNum = int(RouteF.readline())
    print ("total Number of router ", ttlRNum)
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
    print "add cost finished"
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
        rNum, r1,r2,newCost = l.split()
        eventDetails = [int(rNum), int(r1), int(r2), int(newCost)]
        eventlist.append(eventDetails)
        roundlist.append(int(rNum))
        l = eventF.readline()
    if (len(roundlist)>0):
        final_event = max(roundlist)
    else:
        final_event = -1
    return eventlist,roundlist,final_event
# The method to update event that read from file
# def update_event(r1, r2, cost, iteration):
#     update_dv = None
#     if (self.id == r1):
#         update_dst = r2
#     elif (self.id == r2):
#         update_dst = r1
#     else:
#         return
#     update_dv_list = []
#     if (cost == -1):
#         cost = None
#         update_dv = DV(self.id, update_dst, cost, None, None)
#         update_dv_list.append(update_dv)
#         for i in range(len(self.table[update_dst - 1])):
#             self.table[update_dst - 1][i] = DV(update_dst, i + 1, None, None, None)
#             update_dv_list.append(DV(update_dst, i + 1, None, None, None))
#         del self.AdjList[update_dst]
#     else:
#         old_cost = self.AdjList[update_dst]
#         self.AdjList[update_dst] = cost
#         update_dv = DV(self.id, update_dst, cost, update_dst, 1)
#         update_dv_list = [update_dv]
#     self.new_update_table(update_dv_list, iteration)
def printNet(network,numIter,outFile):
    outFile.write("Round: %d"%numIter)
    print ("Round: %d"%numIter)
    for idx,router in network.items():
        outFile.write(router.toString(len(network)))
        print (router.toString(len(network)))
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
    eventlist,roundlist,max_event = iniEvent(eventFile)
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
    numIterations = 0
    converged = False
    eventlist_counter = 0
   
    while converged == False or numIterations <= max_event:
        event_trigger = False
        if (numIterations in roundlist):
            r1 = eventlist[eventlist_counter][1]
            r2 = eventlist[eventlist_counter][2]

            newCost = eventlist[eventlist_counter][3]
            network[r1].updateCost(r2,newCost)
            network[r2].updateCost(r1,newCost)

            eventlist_counter+=1
            event_trigger = True;

        #basic
        Overchanged = False
        if flag == 1:
            printNet(netWorkbasic,numIterations,basicF)
        for srcNum,srcRouter in netWorkbasic.items():
             for destNum,destRouter in netWorkbasic.items():
                localChanged = False
                nextHop,minCost = srcRouter.destTable[destNum]
                
                for adjNum in srcRouter.AdjList:
                    adjCost = srcRouter.costList[adj]
                    adjDest = netWorkbasic[adj].destTable[destNum][1]
                    disFromAdj = adjDest + adjCost
                    if disFromAdj < minCost:
                        minCost = disFromAdj
                        nextHop = adjNum
                        changed = True
                        localChanged = True
                if localChanged:
                    srcRouter.updateDest(destNum,nextHop,minCost)

        break
    basicF.close()

if __name__ == "__main__":
    programStart(sys.argv)
