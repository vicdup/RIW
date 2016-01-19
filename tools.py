# -*- coding: utf-8 -*-
from collections import defaultdict
import re
import time
import json

def tokenisation(text):
    return re.findall(r"[\w]+", text)


def lemmatisation(word):
    return word


def rec_dd():
    return defaultdict(rec_dd)

def writeToDisk(var, name):
	print "Ecriture de " + name + " sur le disque"
	t0 = time.clock()
	with open(name, 'w') as outfile:
		json.dump(var, outfile, sort_keys=True,indent=4, separators=(',', ': '))
	t1=time.clock()
	print "Fichier écrit en ", t1 - t0, "secondes"
	return t1-t0