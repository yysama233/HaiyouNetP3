import sys
from collections import defaultdict
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
    print netWork
    for i, router in netWork.items():
        print i, ":" ,router.AdjList
    return netWork

if __name__ == "__main__":
    iniRouter(sys.argv[1])