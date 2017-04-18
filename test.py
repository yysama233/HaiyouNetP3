import sys
from collections import defaultdict
class Router(object):
    def __init__(self,num):
        self.num = num
        self.AdjList = []
        self.table = []
        self.interation = 0;
        self.updated = False;
        self.destRoute[dest] = defaultdict(lambda: float('inf'))
        self.costList = dict()
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
    for i in range(1, ttlRNum + 1):
        tempR = Router(i)
        netWork[i] = tempR
    for line in RouteF.readlines():
        r1,r2,cost = line.split()
        netWork[int(r1)].addAdj(int(r2),int(cost))
        netWork[int(r2)].addAdj(int(r1),int(cost))
    print netWork
    for i, router in netWork.items():
        print i, ":" ,router.AdjList
    return netWork


def programStart(argv):
    if (len(argv)!= 4):
       print("Invalid arguments")
       sys.exit()
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

    #algorithm
    
if __name__ == "__main__":
    print sys.argv
    programStart(sys.argv)