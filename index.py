# -*- coding: utf-8 -*-
import json
import math
import time
from tools import *


class Index:

    'Index class'

    def __init__(self, source, comonwords):
        self.source = source
        self.comonwords = comonwords

    def generateIndex(self):
        index = {}
        separateurs = ['.T', '.W', '.K']
        commonWords = self.generateListCW()
        for id in self.dico:
            for sep in separateurs:
                if (sep in self.dico[id].keys()):
                    if (id not in index.keys()):
                        index[id] = {}
                    for word in tokenisation(self.dico[id][sep].lower()):
                        if (word not in commonWords):
                            # TODO lemmatisation
                            word = lemmatisation(word)
                            if (word not in index[id].keys()):
                                index[id][word] = 1
                            else:
                                index[id][word] += 1
        with open('index.json', 'w') as outfile:
            json.dump(index, outfile)
        self.index = index
        return len(index.keys())

    def indexText(self, text):
        commonWords = self.generateListCW()
        index = rec_dd()
        textWeight = 0
        for word in tokenisation(text.lower()):
            if (word not in commonWords):
                # TODO lemmatisation
                word = lemmatisation(word)
                textWeight += 1
                if index[word]:
                    index[word]['count'] += 1
                else:
                    index[word]['count'] = 1
        for word in index.keys():
            index[word]['weight'] = index[word][
                'count'] / math.sqrt(float(textWeight))
        return index

    def generateIIndex(self):
        iIndex = rec_dd()
        t1 = time.clock()
        self.generateIndex()
        t2= time.clock()
        print 'index genéré en ' + str(t2 - t1) + 's'
        dicoWeights=rec_dd()
        #Un premier passage permet de remplir l'index inverse avec la frequence et le total
        for article in self.index.keys():
            articleWeight = 0
            # Calcul du poids de l'article en cours
            for mot in self.index[article].keys():
                # En frequence
                articleWeight += math.pow(self.index[article][mot], 2)
            dicoWeights[article]['frequence']=articleWeight
            # Calcul du poids du mot dans l'article
            for mot in self.index[article].keys():
                # Calcul de la frequence (=nb occurence)
                iIndex[mot]['poids'][article][
                    'count'] = self.index[article][mot]
                # Calcul du nombre total d'occurence du mot dans la collection
                if iIndex[mot]['total']:
                    iIndex[mot]['total'] += self.index[article][mot]
                else:
                    iIndex[mot]['total'] = self.index[article][mot]
        #Un deuxieme passage permet de calculer les poids tf-idf des articles
        for article in self.index.keys():
            articleTfIdf = 0
            articleProba = 0
            for mot in self.index[article].keys():
                # Calcul du poids de l'article en tf-idf
                a = self.index[article][mot]
                b = len(self.index.keys())
                c = iIndex[mot]['total']
                articleTfIdf += math.pow((1 + math.log10(a)) * math.log10(b / c), 2)
                dicoWeights[article]['tf-idf']=articleTfIdf

                articleProba += math.pow(math.log10(b/c),2)
                dicoWeights[article]['proba']=articleProba
            # Dernier passage pour calculer les poids des mots dans les articles normalises
        for article in self.index.keys():
            for mot in self.index[article].keys():
                # Calcul de tf simple normalise
                if dicoWeights[article]['frequence'] != 0:
                    iIndex[mot]['poids'][article]['tf'] = self.index[article][mot] / math.sqrt(float(dicoWeights[article]['frequence']))
                # Calcul de tf-idf en log et normalise
                if iIndex[mot]['total'] != 0 and dicoWeights[article]['tf-idf'] != 0:

                    iIndex[mot]['poids'][article]['tf-idf'] = (1 + math.log10(iIndex[mot]['poids'][article]['count'])) * math.log10(
                        len(self.index.keys()) / iIndex[mot]['total']) / math.sqrt(dicoWeights[article]['tf-idf'])
                        
                if dicoWeights[article]['proba'] != 0:
                    iIndex[mot]['poids'][article]['proba'] = math.log10(len(self.index.keys()) / iIndex[mot]['total']) / math.sqrt(dicoWeights[article]['proba'])
        print 'index inverse généré en ' + str(time.clock() - t2) +'s'
        with open('iIndex.json', 'w') as outfile:
            json.dump(iIndex, outfile, sort_keys=True,indent=4, separators=(',', ': '))

        self.iIndex = iIndex
        return len(iIndex.keys())

    def generateListCW(self):
        lComonWords = []
        with open(self.comonwords, 'r') as CW:
            for word in CW:
                lComonWords += [word[:-1]]
        return lComonWords

    def generateDico(self):
        articles = {}
        article = {}
        id = -1
        separateurs = ['.I', '.V', '.T', '.W', '.B', '.A', '.N', '.X', '.K']
        with open(self.source, 'r') as cacm:
            for line in cacm:
                if (line[0:2] == ".I"):
                    if (id != -1):
                        articles[id] = article
                        article = {}
                    id = int(line[3:])
                elif (line[0:2] in separateurs):
                    delimiteur = line[0:2]
                elif (line[0:2] not in separateurs and id != -1 and
                      delimiteur != '.I'):
                    if (delimiteur in article.keys()):
                        if (delimiteur == '.A'):
                            article[delimiteur] = article[
                                delimiteur] + [line.replace('\n', '')]
                        else:
                            article[delimiteur] = article[
                                delimiteur] + line.replace('\n', ' ')
                    else:
                        if (delimiteur == '.A'):
                            article[delimiteur] = [line.replace('\n', '')]
                        else:
                            article[delimiteur] = line.replace('\n', ' ')
            articles[id] = article
        self.dico = articles
        return len(articles)

   
    def loadIndexFromFile(self):
        try:
            with open('index.json') as data_file:
                self.index = json.load(data_file)
                print "Index correctement charge " + str(len(self.index.keys())) + " clefs"
        except Exception, e:
            raise e

    def loadIIndexFromFile(self):
        try:
            with open('iIndex.json') as data_file:
                self.iIndex = json.load(data_file)
                print "Index inverse correctement charge " + str(len(self.iIndex.keys())) + " clefs"
        except Exception, e:
            raise e

