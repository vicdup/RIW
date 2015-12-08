import re
import json
from tools import *

class Index:
	'Index class'
	def __init__(self, source, comonwords):
		self.source=source
		self.comonwords=comonwords

	def generateIndex(self):
		index = {}
		dico = self.generateDico()
		separateurs = ['.T','.W','.K']
		commonWords = self.generateListCW()
		for id in dico:
			for sep in separateurs:
				if (sep in dico[id].keys()):
					if (id not in index.keys()):
						index[id]={}
					for word in tokenisation(dico[id][sep].lower()):
						if (word not in commonWords):
							#TODO lemmatisation
							word = lemmatisation(word)
							if (word not in index[id].keys()):
								index[id][word]=1
							else:
								index[id][word]+=1
		self.index=index
		return len(index.keys())

	def generateInverseIndex(self):
		index = rec_dd()
		dico = self.generateDico()
		separateurs = ['.T','.W','.K']
		commonWords = self.generateListCW()
		for id in dico:
			for sep in separateurs:
				if (sep in dico[id].keys()):
					for word in tokenisation(dico[id][sep].lower()):
						if (word not in commonWords):
							#TODO lemmatisation
							word = lemmatisation(word)
							if index[word][id]['count']:
								index[word][id]['count']+=1
							else:
								index[word][id]['count']=1
		self.iIndex=index
		return len(index.keys())

	def generateListCW(self):
		lComonWords =[]
		with open(self.comonwords, 'r') as CW:
			for word in CW:
				lComonWords+=[word[:-1]];
		return lComonWords

	def generateDico(self):
		articles = {}
		article = {}
		record =0
		id = -1
		text = ''
		separateurs = ['.I','.T','.W','.B','.A','.N','.X','.K']
		with open(self.source, 'r') as cacm:
			for line in cacm:
				if (line[0:2]==".I"):
					if (id<>-1):
						articles[id] = article
						article={}
					id = int(line [3:])
				elif (line[0:2] in separateurs):
					delimiteur = line[0:2]
				elif (line[0:2] not in separateurs and id <>-1 and delimiteur <>'.I'):
					if (delimiteur in article.keys()):
						if (delimiteur == '.A'):
							article[delimiteur]=article[delimiteur]+[line.replace('\n', '')]
						else:
							article[delimiteur]=article[delimiteur]+line.replace('\n', ' ')
					else:
						if (delimiteur == '.A'):
							article[delimiteur]=[line.replace('\n', '')]
						else:
							article[delimiteur]=line.replace('\n', ' ')
			articles[id] = article
		return articles