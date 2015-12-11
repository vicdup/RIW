import re
import json
from tools import *


class Index:
    'Index class'

    def __init__(self, source, comonwords):
        self.source = source
        self.comonwords = comonwords

    def generateIndex(self):
        index = {}
        dico = self.generateDico()
        separateurs = ['.T', '.W', '.K']
        commonWords = self.generateListCW()
        for id in dico:
            for sep in separateurs:
                if (sep in dico[id].keys()):
                    if (id not in index.keys()):
                        index[id] = {}
                    for word in tokenisation(dico[id][sep].lower()):
                        if (word not in commonWords):
                            # TODO lemmatisation
                            word = lemmatisation(word)
                            if (word not in index[id].keys()):
                                index[id][word] = 1
                            else:
                                index[id][word] += 1
        with open('index.json', 'w') as outfile:
			json.dump(index, outfile)
        self.index=index
        return len(index.keys())

    def generateIIndex(self):
        iIndex = rec_dd()
        self.generateIndex()
        for article in self.index.keys():
            articleWeight = 0
            for mot in self.index[article].keys():
                articleWeight += self.index[article][mot]
            for mot in self.index[article].keys():
                iIndex[mot][article]['count'] = self.index[article][mot]
                if articleWeight != 0:
                    iIndex[mot][article]['weight'] = self.index[article][mot] / float(articleWeight)

        with open('iIndex.json', 'w') as outfile:
			json.dump(iIndex, outfile)

        self.iIndex=iIndex
        return len(iIndex.keys())

    # def generateInverseIndex(self):
    # 	iIndex = rec_dd()
    # 	dico = self.generateDico()
    # 	separateurs = ['.T','.W','.K']
    # 	commonWords = self.generateListCW()
    # 	for id in dico:
    # 		for sep in separateurs:
    # 			if (sep in dico[id].keys()):
    # 				for word in tokenisation(dico[id][sep].lower()):
    # 					if (word not in commonWords):
    # 						#TODO lemmatisation
    # 						word = lemmatisation(word)
    # 						if iIndex[word][id]['count']:
    # 							iIndex[word][id]['count']+=1
    # 						else:
    # 							iIndex[word][id]['count']=1
    # 	self.iIndex=iIndex
    # 	return len(iIndex.keys())

    def generateListCW(self):
        lComonWords = []
        with open(self.comonwords, 'r') as CW:
            for word in CW:
                lComonWords += [word[:-1]];
        return lComonWords

    def generateDico(self):
        articles = {}
        article = {}
        record = 0
        id = -1
        text = ''
        separateurs = ['.I', '.T', '.W', '.B', '.A', '.N', '.X', '.K']
        with open(self.source, 'r') as cacm:
            for line in cacm:
                if (line[0:2] == ".I"):
                    if (id <> -1):
                        articles[id] = article
                        article = {}
                    id = int(line[3:])
                elif (line[0:2] in separateurs):
                    delimiteur = line[0:2]
                elif (line[0:2] not in separateurs and id <> -1 and delimiteur <> '.I'):
                    if (delimiteur in article.keys()):
                        if (delimiteur == '.A'):
                            article[delimiteur] = article[delimiteur] + [line.replace('\n', '')]
                        else:
                            article[delimiteur] = article[delimiteur] + line.replace('\n', ' ')
                    else:
                        if (delimiteur == '.A'):
                            article[delimiteur] = [line.replace('\n', '')]
                        else:
                            article[delimiteur] = line.replace('\n', ' ')
            articles[id] = article
        return articles

    def loadIndexFromFile(self):
    	try:
    		with open('index.json') as data_file:    
				self.index = json.load(data_file)
    	except Exception, e:
    		raise e

	def loadIIndexFromFile(self):
		try:
			with open('iIndex.json') as data_file:    
				self.iIndex = json.load(data_file)
		except Exception, e:
			raise e