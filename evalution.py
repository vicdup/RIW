from tools import *

def parseQrels(qrels):
	parsedQrels = rec_dd()
	with open(qrels, 'r') as qrels:
		for line in qrels:
			if parsedQrels[int(line[0:2])]:
				parsedQrels[int(line[0:2])] += [int(line [3:7])]
			else:
				parsedQrels[int(line[0:2])] = [int(line [3:7])]
			# parsedQrels[int(line[0:2])] = line [4:7]
	return parsedQrels

def calculRappel(results, pertinents, k):
	rappel = float(0)
	for doc in results[:k]:
		if doc in pertinents:
			rappel += 1.0*1/len(pertinents)
	return rappel

def calculPrecision(results, pertinents, k):
	precision = float(0)
	for doc in results[:k]:
		if doc in pertinents:
			precision += 1.0*1/k
	return precision