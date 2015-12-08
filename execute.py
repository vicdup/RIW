from index import *
from search import *
import sys 
import json

source = 'CACM\cacm.all'
commonwords= 'CACM\common_words'




index = Index(source,commonwords)
index.generateInverseIndex()
#print index.iIndex
search = Search('bool')
print sys.getsizeof(index.iIndex)
#print json.dumps(index.iIndex)
print len(index.iIndex.keys())

search.setQuery('computer AND computer')
print search.booleanSearch(index.iIndex)