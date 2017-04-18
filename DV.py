from string import *
import sys
from collections import defaultdict
from __future__ import print_function

class distanceVector:
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
    def to_string(self):
        print("(Distance vector", self.src, self.dst, self.cost, self.next_hop, self.num_hops, ")\t", end= '')

class Router(object):
    def __init__(self,num):
        self.num = num
        self.AdjList = []
        #the distance to route num
        self.interation = 0;
        self.updated = False;
        self.costList = defaultdict(lambda: float('inf'))
    def getDist(self,dest):
        return self.destRoutes[dest]
    def addRoute(self,dest,dist):
        self.destRoutes[dest]=dist
    def addAdj(self,dest,cost):
        self.AdjList.append(dest)
        self.costList[dest]=cost
    def rmRoute(self,dest):
        del destRoutes[dest]

def iniRouter(routerFile):
    try:
        RouteF = open(routerFile,'r')
    except:
        print("Invalid file")
        sys.exit()
    netWork ={}
    ttlRNum = int(RouteF.readline())
    for i in range(0, ttlRNum + 1):
        tempR = Router(i)
        netWork[i] = tempR
    for line in RouteF.readlines():
        r1,r2,cost = line.split()
        netWork[int(r1)].addAdj(int(r2),int(cost))
        netWork[int(r2)].addAdj(int(r1),int(cost))
    return netWork

def new_update_table(self,new_datavector_list,iternum):
    for dv in new_datavector_list:
        #change the line in original table accordingly

    for i in range

def update_event(self, src, dst, cost, iteration):
    update_dv = None
    if (self.id == src):
        update_dst = dst
    elif (self.id == dst):
        update_dst = src
    else:
        return
    update_dv_list = []
    if (cost == -1):
        cost = None
        update_dv = distanceVector(self.id, update_dst, cost, None, None)
        update_dv_list.append(update_dv)
        for i in range(len(self.table[update_dst - 1])):
            #self.table[update_dst - 1][i] = distanceVector(update_dst, i + 1, None, None, None)
            update_dv_list.append(distanceVector(update_dst, i + 1, None, None, None))
        del self.neighbors[update_dst]
    else:
        old_cost = self.neighbors[update_dst]
        self.neighbors[update_dst] = cost
        update_dv = distanceVector(self.id, update_dst, cost, update_dst, 1)
        update_dv_list = [update_dv]

    self.new_update_table(update_dv_list, iteration)

def programStart(argv):
    #if (len(argv)!=4):
    #    print("Invalid arguments")
    #    sys.exit()
    routerFile = argv[1]
    netWork = iniRouter(routerFile)
    if not netWork:
        print("invalid router file")
        sys.exit()

    eventFile = argv[2]
    eventf = open(eventFile,"r")
    eventinput = eventf.readlines()
    eventlist = []
    roundlist = []
    for l in eventinput:
        newvec = l.split()
        eventDetails = [int(newvec[0]), int(newvec[1]), int(newvec[2]), int(newvec[3])]
    	eventlist.append(eventDetails)
        roundlist.append(int(newvec[0]))
    if (len(roundlist)>0):
        max_event = max(roundlist)
    else:
        max_event = -1


#start of the first ALGORITHM
    numIterations = 0
    converged = False;
    eventlist_counter = 0;
    print(".......1st ALGORITHM......")
    while converged == False or numIterations <= max_event
        event_trigger = False
        if (numIterations in roundlist):
            for router in netWork:
                firstarg = eventlist[eventlist_counter][1];
                secarg = eventlist[eventlist_counter][2];
                thirdarg = eventlist[eventlist_counter][3]
                router.update_event(numIterations, firstarg,secarg,thirdarg)
            eventlist_counter++;
            event_trigger = True;
        oldnetWork = [];
        for router in netWork:
            oldnetWork.append(copy.deepcopy(router))
            for neighbor in router.AdjList:
                if router.num > netWork[neighbor - 1].num:
                    router.new_update_table()
                else:
                    router.new_update_table();
        numIteration++

        numUpdate = 0;
        for router in netWork:
            if rounter.updated == 0:
                numUpdate++
        if numUpdate == len(netWork):
            converged = True


if __name__ == "__main__":
    programStart(sys.argv)
