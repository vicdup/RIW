import re


def toDico(path):
	articles = {}
	article = {}
	record =0
	id = -1
	text = ''
	separateurs = ['.I','.T','.W','.B','.A','.N','.X','.K']
	with open(path, 'r') as cacm:
		for line in cacm:
			if (line[0:2]==".I"):
				if (id<>-1):
					articles[id] = article
					article={}
			 	id = int(line [3:])
			elif (line[0:2] in separateurs):
				delimiteur = line[0:2]
			elif (line[0:2] not in separateurs and id <>-1 and delimiteur <>'.I'):
				article[delimiteur]=line.replace('\n', ' ')
		articles[id] = article
	return articles

print toDico('CACM\cacm.all')[3204]