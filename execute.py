
import search
import index
import json

source = 'CACM\cacm.all'
commonwords = 'CACM\common_words'

# index.generateInverseIndex()
# print index.iIndex
# print sys.getsizeof(index.iIndex)
# print json.dumps(index.iIndex)
# print len(index.iIndex.keys())

# print json.dumps(index.iIndex)
# print search.booleanSearch(index.iIndex)
# vectorA = {"victor": 10, "pauline": 5, "matthieu": 3, "aurore": 12}
# vectorB = {"victor": 2, "pauline": 0, "matthieu": 3, "aurore": 12}

# print search.calculCosinus(vectorA,vectorB)
# index.generateIIndex()
# index.generateIndex()
# import operator
# index.generateIIndex()
search = search.Search('tf')
search.setQuery('What articles exist which deal with TSS (Time Sharing System), an operating system for IBM computers?')
index = index.Index(source, commonwords)
index.loadIIndexFromFile()
search.presentResults(search.vectorielSearch(index.iIndex))
print index.generateDico()[398]['.T']

#Pogres : 
# Tf-Idf ok mais renvoie en priorité les articles vides, à voir comment gérer ça dans les poids