from string import *
import sys
from collections import defaultdict
from __future__ import print_function

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
    def to_string(self):
        print("(Distance vector", self.src, self.dst, self.cost, self.next_hop, self.num_hops, ")\t", end= '')

class Router(object):
    def __init__(self,num):
        self.num = num
        self.AdjList = []
        self.table = []
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

    def Initialize_router_table(number_of_routers):
        self.table = []
        for r in range(number_of_routers):
            self.table.append([])
            #the row of itself
            if(r == (self.num - 1)):
                for i in range(number_of_routers):
                    if (i==(self.num-1)):
                        self.table[r].append(DV(self.num, self,num, 0 , None, 0))
                    elif((i+1) in self.AdjList):
                        self.table[r].append(DV(self.num, (i+1), getDist(self.AdjList[i+1]), (i+1), 1))
                    else
                        not_existing = DV(self.num, (i+1), None, None, None)
                        self.table[r].append(not_existing)
            else:
                for i in range(number_of_routers):
                    not_existing = DV(r+1, i+1, None, None,None)
                    self.table[r].append(not_existing)

    def new_update_table(self, dv_list, iteration, old_cost = 0, flag = False):

        for dv in dv_list:
            self.table[dv.src - 1][dv.dst - 1] = dv

        for i in range(len(self.table[self.id - 1])):
            old_dv = self.table[self.id - 1][i]
            dv = self.table[self.id - 1][i]
            if (dv.dst != self.id):
                dv_min = None
                min_cost = None
                dv_min_set = False
                #pick the smallest path to the dst among all neighbors
                for adjlist in self.neighbors:
                    if (dv_min_set == False and self.table[AdjList - 1][dv.dst - 1].cost is not None):
                        dv_min_set = True
                        dv_min = self.table[AdjList - 1][dv.dst - 1]
                        min_cost = self.table[AdjList - 1][dv.dst - 1].cost + self.adjList[adjlist]
                    elif (self.table[adjlist - 1][dv.dst - 1].cost is not None and
                        self.table[adjlist - 1][dv.dst - 1].cost + self.adjList[adjlist] < min_cost):
                        dv_min = self.table[adjlist - 1][dv.dst - 1]
                        min_cost = self.table[adjlist - 1][dv.dst - 1].cost + self.adjList[adjlist]

                if (not dv_min_set):
                    none_dv = DV(self.id, dv.dst, None, None, None)
                    self.table[self.num - 1][dv.dst - 1] = none_dv

                elif (dv.dst in self.adjList and self.adjList[dv.dst] < min_cost):
                    print("result")
                    to_string(dv_min)
                    print("")
                    src = self.id
                    dst = dv_min.dst
                    cost = self.adjList[dv.dst]
                    next_hop = dv.dst
                    num_hops = 1
                    self.table[self.num - 1][dv.dst - 1] = DV(src, dst, cost, next_hop, num_hops)
                else:
                    print("result, min cost", min_cost)
                    to_string(dv_min)
                    print("")
                    src = self.id
                    dst = dv_min.dst
                    cost = min_cost
                    next_hop = dv_min.src
                    num_hops = dv_min.num_hops + 1
                    self.table[self.num - 1][dv.dst - 1] = DV(src, dst, cost, next_hop, num_hops)
                if (old_dv == self.table[self.num - 1][dv.dst - 1]):

                    self.set_update(0, iteration)
                else:

                    self.set_update(1, iteration)

                if (min_cost > 100):
                    print("Convergence instability")
                    exit()


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
        update_dv = DV(self.id, update_dst, cost, None, None)
        update_dv_list.append(update_dv)
        for i in range(len(self.table[update_dst - 1])):
            self.table[update_dst - 1][i] = DV(update_dst, i + 1, None, None, None)
            update_dv_list.append(DV(update_dst, i + 1, None, None, None))
        del self.AdjList[update_dst]
    else:
        old_cost = self.AdjList[update_dst]
        self.AdjList[update_dst] = cost
        update_dv = DV(self.id, update_dst, cost, update_dst, 1)
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
