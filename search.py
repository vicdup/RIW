from tools import *

class Search:
	possibleTypes=['bool']

	def __init__(self, type):
		if (type in self.possibleTypes):
			self.type = type
		else:
			raise ValueError('unknown search type')

	def setType(self,type):
		if (type in self.possibleTypes):
			self.type = type
		else:
			raise ValueError('unknown search type')
	def setQuery(self,query):
			self.query = query
			print 'Quey set to '+query
			return 0

	def getPostingFromIndexInverse(self, index, word):
		return index[word].keys()

	def andPosting(self,a,b):
		return list(set(a) & set(b))

	def orPosting(self,a,b):
		return list(set(a) | set(b))

	def notPosting(self,a,b):
		return list(set(a) - set(b))

	def booleanSearch(self, indexInverse):
		operators = ['AND', 'OR', 'NOT']
		tquery=tokenisation(self.query)
		posts=self.getPostingFromIndexInverse(indexInverse,tquery[0])
		for i in range(len(tquery)):
			if tquery[i] == 'AND':
				posts=self.andPosting(posts,self.getPostingFromIndexInverse(indexInverse,tquery[i+1]))
			if tquery[i] == 'OR':
				posts=self.orPosting(posts,self.getPostingFromIndexInverse(indexInverse,tquery[i+1]))
			if tquery[i] == 'NOT':
				posts=self.notPosting(posts,self.getPostingFromIndexInverse(indexInverse,tquery[i+1]))
		return posts