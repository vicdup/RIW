
import search
import sys
import json
import index

source = 'CACM\cacm.all'
commonwords = 'CACM\common_words'

# index.generateInverseIndex()
# print index.iIndex
search = search.Search('bool')
# print sys.getsizeof(index.iIndex)
# print json.dumps(index.iIndex)
# print len(index.iIndex.ke	ys())
# index.generateIIndex()
# print json.dumps(index.iIndex)
# search.setQuery('computer AND computer')
# print search.booleanSearch(index.iIndex)
# vectorA = {"victor": 10, "pauline": 5, "matthieu": 3, "aurore": 12}
# vectorB = {"victor": 2, "pauline": 0, "matthieu": 3, "aurore": 12}

# print search.calculCosinus(vectorA,vectorB)
# index.generateIIndex()
# index.generateIndex()

index = index.Index(source, commonwords)
index.loadIndexFromFile()
