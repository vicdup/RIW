from tools import *
import math
import index
from index import *
import operator


class Search:
    possibleTypes = ['bool','tf','tf-idf']

    def setType(self, type):
        if (type in self.possibleTypes):
            self.type = type
        else:
            raise ValueError('unknown search type')

    def setQuery(self, query):
        self.query = query
        # print 'Quey set to ' + query
        return 0

    def getPostingFromIndexInverse(self, index, word):
        return index[word]['poids'].keys()

    def andPosting(self, a, b):
        return list(set(a) & set(b))

    def orPosting(self, a, b):
        return list(set(a) | set(b))

    def notPosting(self, a, b):
        return list(set(a) - set(b))

    def booleanSearch(self, indexInverse):
        tquery = tokenisation(self.query)
        posts = self.getPostingFromIndexInverse(indexInverse, tquery[0])
        for i in range(len(tquery)):
            if tquery[i] == 'AND':
                posts = self.andPosting(
                    posts, self.getPostingFromIndexInverse
                    (indexInverse, tquery[i + 1]))
            if tquery[i] == 'OR':
                posts = self.orPosting(
                    posts, self.getPostingFromIndexInverse
                    (indexInverse, tquery[i + 1]))
            if tquery[i] == 'NOT':
                posts = self.notPosting(
                    posts, self.getPostingFromIndexInverse
                    (indexInverse, tquery[i + 1]))
        return posts

    def vectorielSearch(self, indexInverse):
        source = 'CACM\cacm.all'
        commonwords = 'CACM\common_words'
        indexedQueryObject = index.Index(source, commonwords)
        indexedQuery = indexedQueryObject.indexText(self.query)
        tableauArticle=[]
        results = rec_dd()
        for mot in indexedQuery.keys():

            if mot in indexInverse.keys():
                for article in indexInverse[mot]['poids'].keys():
                    if article not in tableauArticle:
                        tableauArticle += [article]
                    if results[article]:
                        if self.type == 'tf':
                            results[article] += indexedQuery[mot][
                                'weight'] * indexInverse[mot]['poids'][article]['tf']
                        elif self.type == 'tf-idf':
                            results[article] += indexedQuery[mot][
                                'weight'] * indexInverse[mot]['poids'][article]['tf-idf']
                    else:
                        if self.type == 'tf':
                            results[article] = indexedQuery[mot][
                                'weight'] * indexInverse[mot]['poids'][article]['tf']
                        elif self.type == 'tf-idf':
                            results[article] = indexedQuery[mot][
                                'weight'] * indexInverse[mot]['poids'][article]['tf-idf']
        return sorted(results.items(), key=operator.itemgetter(1), reverse=True)[:self.resultsLimit]

    def presentResults(self, results):
        sorted_results = sorted(
            results.items(), key=operator.itemgetter(1), reverse=True)
        i = 1
        for result in sorted_results:
            print str(i) + " : " + result[0] + " with a score of " + str(result[1])
            i += 1
            if i>30:
                break
        return sorted_results

    def calculCosinus(self, vectorB):
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
            return produitcroise / (math.sqrt(sommeCarreA) + math.sqrt
                                    (sommeCarreB))
        return 0

    def setLimit(self, limit):
        self.resultsLimit = limit
