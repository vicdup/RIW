# -*- coding: utf-8 -*-
import search
import index
import json
import csv
from evalution import *
from tools import *

sourceEval = 'CACM\query.text'
source = 'CACM\cacm.all'
commonwords = 'CACM\common_words'

####
####
# Generation de l'index sur CACM
####
####

source = 'CACM\cacm.all'
commonwords = 'CACM\common_words'

cacm = index.Index(source, commonwords)
# Parsing de la source pour en faire un dico
cacm.generateDico()
# Creation de l'index inverse (comprends la creation de l'index)
# cacm.generateIIndex()
cacm.loadIIndexFromFile()

###
###
# Lancement d'une recherche
###
###

recherche = search.Search()
recherche.setType('tf-idf')

####
####
# Evaluation des algorithmes
####
####
qrels= 'CACM\qrels.text'
parsedQrels=parseQrels(qrels)

### Mise sous forme de dictionnaire du fichier query.text
resultatsEvaluation=rec_dd()

sourceEval = 'CACM\query.text'
commonwords = 'CACM\common_words'
f = csv.writer(open("evaluation.csv", "wb+"))

evaluation = index.Index(sourceEval, commonwords)
evaluation.generateDico()

for requete in evaluation.dico:
	recherche.setQuery(evaluation.dico[requete]['.W'])
	recherche.setLimit(20)
	resultsScored = recherche.vectorielSearch(cacm.iIndex)
	results = [int(result[0]) for result in resultsScored]
	for k in [1,5,10,20]:
		# print results
		# print parsedQrels[requete]
		if parsedQrels[requete]:
			resultatsEvaluation[requete][k]['rappel'] = calculRappel(results, parsedQrels[requete],k) 
			resultatsEvaluation[requete][k]['precision'] = calculPrecision(results, parsedQrels[requete],k) 
header = ['requete','ordre','rappel','precision']
f.writerow(header)
for requete in resultatsEvaluation:
	for ordre in resultatsEvaluation[1]:
		row = [requete]
		row += [ordre]
		for data in ['rappel','precision']:
			row += [resultatsEvaluation[requete][ordre][data]]
		f.writerow(row)