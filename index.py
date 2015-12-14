import json
import math
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
        self.generateIndex()
        for article in self.index.keys():
            articleWeight = 0
            articleTfIdf = 0
            # Calcul du poids de l'article en cours
            for mot in self.index[article].keys():
                # En frequence
                articleWeight += math.pow(self.index[article][mot], 2)
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
            for mot in self.index[article].keys():
                # Calcul du poids de l'article en tf-idf
                articleTfIdf += math.pow((1 + math.log10(float(self.index[article][mot]))) * math.log10(
                    float(len(self.index.keys())) / float(iIndex[mot]['total'])), 2)
            # Calcul du poids du mot dans l'article
            for mot in self.index[article].keys():
                # Calcul de tf simple normalise
                if articleWeight != 0:
                    iIndex[mot]['poids'][article]['tf'] = self.index[article][mot] / math.sqrt(float(articleWeight))
                # Calcul de tf-idf en log et normalise
                if iIndex[mot]['total'] != 0 and articleTfIdf != 0:
                    iIndex[mot]['poids'][article]['tf-idf'] = (1 + math.log10(iIndex[mot]['poids'][article]['count'])) * math.log10(
                        len(self.index.keys()) / iIndex[mot]['total']) / math.sqrt(articleTfIdf)
        with open('iIndex.json', 'w') as outfile:
            json.dump(iIndex, outfile)

        self.iIndex = iIndex
        return len(iIndex.keys())

    # def generateInverseIndex(self):
    #   iIndex = rec_dd()
    #   dico = self.generateDico()
    #   separateurs = ['.T','.W','.K']
    #   commonWords = self.generateListCW()
    #   for id in dico:
    #       for sep in separateurs:
    #           if (sep in dico[id].keys()):
    #               for word in tokenisation(dico[id][sep].lower()):
    #                   if (word not in commonWords):
    # TODO lemmatisation
    #                       word = lemmatisation(word)
    #                       if iIndex[word][id]['count']:
    #                           iIndex[word][id]['count']+=1
    #                       else:
    #                           iIndex[word][id]['count']=1
    #   self.iIndex=iIndex
    #   return len(iIndex.keys())

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
        separateurs = ['.I', '.T', '.W', '.B', '.A', '.N', '.X', '.K']
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
