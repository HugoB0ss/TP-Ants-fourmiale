import pants
import math
import random
import csv
import sys
import networkx as nx
import matplotlib.pyplot as plt
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
	
	bestSolutionLength = sys.maxsize
	for solution in solutions:
		if solution.distance < bestSolutionLength:
			bestSolution = solution
			bestSolutionLength = solution.distance
		print('Ants colony found a way ! Need %d meters to make it all' % solution.distance)
	print('')
	print('===============================')
	print('Best solution is %d meters' % bestSolution.distance)
	print('===============================')
	return bestSolution;
	
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
		
	#
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
	bestSolution = printSolution(solver,world)
	createGraph(bestSolution)
	input('exit?')
	
def createGraph(solution):
    noeudsVisiter = solution.tour
    G = nx.Graph()
    # G.add_edges_from(noeudsVisiter)
    for noeud in noeudsVisiter:
        G.add_edge(format(noeud[0]), format(noeud[1]), weight=0.6)
    plt.subplot(121)

    node_positions = nx.spring_layout(G)  # positions for all nodes
    nx.draw_networkx(G, pos=node_positions, node_size=100, node_color='red', edge_color="green", with_labels=True,
                     alpha=1)

    edge_labels = nx.get_edge_attributes(G, 'sequence')
    nx.draw_networkx_edge_labels(G, pos=node_positions, edge_labels=edge_labels, font_size=20)
    nx.draw_networkx_nodes(G, pos=node_positions, node_size=20)
    nx.draw_networkx_edges(G, pos=node_positions, alpha=0.4)

    plt.xticks([])
    plt.yticks([])

    plt.text(0.5, 0.5, G, ha="center", va="center", size=24, alpha=.5)
    plt.title('Noeuds Vistées', size=15)

    plt.ylabel("Y")
    plt.xlabel("X")
    plt.axis('off')

    plt.subplot(122)
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    dmax = max(degree_sequence)

    # draw graph in inset
    plt.axis('off')
    plt.show()

	
main()
