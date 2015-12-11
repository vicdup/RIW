from tools import *
import math
from index import *


class Search:
    possibleTypes = ['bool']

    def __init__(self, type):
        if (type in self.possibleTypes):
            self.type = type
        else:
            raise ValueError('unknown search type')

    def setType(self, type):
        if (type in self.possibleTypes):
            self.type = type
        else:
            raise ValueError('unknown search type')

    def setQuery(self, query):
        self.query = query
        print 'Quey set to ' + query
        return 0

    def getPostingFromIndexInverse(self, index, word):
        return index[word].keys()

    def andPosting(self, a, b):
        return list(set(a) & set(b))

    def orPosting(self, a, b):
        return list(set(a) | set(b))

    def notPosting(self, a, b):
        return list(set(a) - set(b))

    def booleanSearch(self, indexInverse):
        operators = ['AND', 'OR', 'NOT']
        tquery = tokenisation(self.query)
        posts = self.getPostingFromIndexInverse(indexInverse, tquery[0])
        for i in range(len(tquery)):
            if tquery[i] == 'AND':
                posts = self.andPosting(posts, self.getPostingFromIndexInverse(indexInverse, tquery[i + 1]))
            if tquery[i] == 'OR':
                posts = self.orPosting(posts, self.getPostingFromIndexInverse(indexInverse, tquery[i + 1]))
            if tquery[i] == 'NOT':
                posts = self.notPosting(posts, self.getPostingFromIndexInverse(indexInverse, tquery[i + 1]))
        return posts

    # def vectorielSearch(self, indexInverse):
    # 	#indexons la query
    # 	indexedQuery = indexQuery(self.query)
    # 	#on parcourt tous les articles et on calcul les cosinus
    # 	for article in indexInverse:


    def calculCosinus(self, vectorA, vectorB):
        # On part du principe que nos deux vecteurs sont des dicos avec {"mot":"poids"}
        # To do : faire la boucle sur le mot qui a le moins de keys
        produitcroise = 0
        sommeCarreA = 0
        sommeCarreB = 0
        for motA in vectorA.keys():
            sommeCarreA += vectorA[motA] * vectorA[motA]
            if motA in vectorB.keys():
                produitcroise += vectorA[motA] * vectorB[motA]
        for motB in vectorB.keys():
            sommeCarreB += vectorB[motB] * vectorB[motB]
        if sommeCarreB + sommeCarreA != 0:
            return produitcroise / (math.sqrt(sommeCarreA) + math.sqrt(sommeCarreB))
        return 0
