# -*- coding: utf-8 -*-
import search
import index
import json
import csv
from evalution import *
from tools import *


def displayMenu():
	print ""
	print ""
	print "1: Indexes related tools"
	print "2: Search related tools"
	print "3: Evaluation related tools"
	print "0: Quit"

def displayIndexesMenu():
	print ""
	print "11: Generate indexes"
	print "12: Read indexes from hard drive"
	print "13: Write current indexes to hard drive"
	print "9: Display main menu"

def displaySearchMenu():
	print ""
	print "21: Define query"
	print "22: Define search mode"
	print "23: Perform the search to console"
	print "23: Perform the search to CSV"
	print "9: Display main menu"

def displayEvaluationMenu():
	print ""
	print "31: Define mode to evaluate"
	print "32: Run evaluation on all the predefined queries"
	print "23: Perform the search to console"
	print "23: Perform the search to CSV"
	print "9: Display main menu"

def makeChoice():
	print ""
	return input("Make a choice: ")

sourceEval = 'CACM\query.text'
source = 'CACM\cacm.all'
commonwords = 'CACM\common_words'
indexFile = 'ressources\index.json'
iIndexFile = 'ressources\iIndex.json'

cacm = index.Index(source, commonwords)
cacm.generateDico()
displayMenu()

while True:
	choice = makeChoice()

	if choice == 0:
		break
	elif choice == 9:
		displayMenu()
	elif choice == 1:
		displayIndexesMenu()
	elif choice == 2:
		displaySearchMenu()
	elif choice ==3:
		displayEvaluationMenu()
	elif choice == 11:
		cacm.generateIndex()
		cacm.generateIIndex()
		displayMenu()
	elif choice ==12:
		cacm.loadIndexFromFile(indexFile)
		cacm.loadIIndexFromFile(iIndexFile)
		displayMenu()
	elif choice ==13:
		writeToDisk(cacm.index,indexFile)
		writeToDisk(cacm.iIndex,iIndexFile)
		displayMenu()
	else:
		displayMenu()