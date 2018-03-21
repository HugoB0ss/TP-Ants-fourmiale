import pants
import math
import random
import csv
import sys
from geopy.distance import vincenty

nodes = []

#Create the map
def createWorld():
	return pants.World(nodes, calculateDistance)
	
#Init the solver
def createSolver():
	return pants.Solver()

#Print the results	
def printSolution(solver,world):
	solutions = solver.solutions(world)
	bestSolution = sys.maxsize
	for solution in solutions:
		if solution.distance < bestSolution:
			bestSolution = solution.distance
		print('Ants colony found a way ! Need %d meters to make it all' % solution.distance)
	print('')
	print('===============================')
	print('Best solution is %d meters' % bestSolution)
	print('===============================')
	
#Calculcate distance using vincenty(geopy) lib for lat/long distance
def calculateDistance(a,b):
	return round(vincenty(a,b).meters)
	
#Open Csv file
def readCsv():
	file = open('test.csv','r')
	return csv.reader(file ,delimiter=',',quotechar='"')
	
#Main function
def main():	
	#init data
	nodesTemp = []
	reader = readCsv()
	nbInvalid = 0
	nbDuplicate = 0
	
	#read csv
	for row in reader:	
		tabRow= row
		try :
			if float(row[len(row) -2])<90 and float(row[len(row) -2])>-90 and float(row[len(row)-3])<180 and float(row[len(row)-3])>-180  :
				nodesTemp.append((float(row[len(row) - 2]),float(row[len(row) -3])))
			else :
				print('errors')
				nbInvalid += 1
		except Exception as e:
			print(e)
			print('error')
			nbInvalid += 1
		
	for elem in nodesTemp:
		if elem not in nodes:
			nodes.append(elem)
		else :
			nbDuplicate += 1
	#for debug
	#print(nodes)
	
	#print the csv parsing result
	print('===============================')
	print('%d valid nodes found in csv' % len(nodes))	
	print('%d invalid nodes found in csv' % nbInvalid)	
	print('%d duplicate geoloc found in csv' % nbDuplicate)	
	print('===============================')
	print('')
	
	world = createWorld()
	solver = createSolver()
	printSolution(solver,world)

	
main()