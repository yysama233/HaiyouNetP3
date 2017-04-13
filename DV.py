from string import *
import sys
class Router(object):
	def __init__(self,num):
		self.num = num
		self.AdjList = []
		#the distance to route num
		self.destRoutes = {num:0}
		self.costList = {num:0}
	def getDist(self,dest):
		if dest in self.destRoutes.keys():
			return self.destRoutes[dest]
		else:
			return sys.maxint

	def addRoute(self,dest,dist):
		self.destRoutes[dest]=dist

	def addAdj(self,dest,cost):
		self.AdjList.append(dest)
		self.costList[dest]=cost
		self.destRoutes[dest]=cost

	def rmRoute(self,dest):
		if dest in self.destRoutes.keys():
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
	routerFile = argv[1]
	netWork = iniRouter(routerFile)
	if not netWork:
		print("invalid router file")
		sys.exit()

if __name__ == "__main__":
    programStart(sys.argv)