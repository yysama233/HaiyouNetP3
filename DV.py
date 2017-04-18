from string import *
import sys
from collections import defaultdict

class Router(object):
    def __init__(self,num):
        self.num = num
        self.AdjList = []
        #the distance to route num
        self.destRoutes = defaultdict(lambda: float('inf'))
        self.destRoutes[num] = 0
        self.costList = defaultdict(lambda: float('inf'))
        self.costList[num] = 0
    def getDist(self,dest):
        return self.destRoutes[dest]

    def addRoute(self,dest,dist):
        self.destRoutes[dest]=dist

    def addAdj(self,dest,cost):
        self.AdjList.append(dest)
        self.costList[dest]=cost
        self.destRoutes[dest]=cost

    def rmRoute(self,dest):
        del destRoutes[dest]

def iniRouter(routerFile):
    try:
        RouteF = open(routerFile,'r')
    except:
        print("Invalid file")
        sys.exit()
    netWork = {}
    ttlRNum = int(RouteF.readline())
    for i in range(1,ttlRNum+1):
        tempR = Router(i)
        netWork[i] = tempR
    for line in RouteF.readlines():
        r1,r2,cost = line.split()
        netWork[r1].addAdj(r2,cost)
        netWork[r2].addAdj(r1,cost)
    return netWork



def programStart(argv):
    if (len(argv)!=4):
        print("Invalid arguments")
        sys.exit()
    #read the router file
    routerFile = argv[1]
    netWork = iniRouter(routerFile)
    #read the change file
    changeFile = argv[2]


    #read the third instruction 0 for no details and 1 for details
    details = argv[3]

    if not netWork:
        print("invalid router file")
        sys.exit()

if __name__ == "__main__":
    programStart(sys.argv)
