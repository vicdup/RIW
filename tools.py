from collections import defaultdict
import re

def tokenisation(text):
	return re.findall(r"[\w]+", text)

def lemmatisation(word):
	return word

def rec_dd():
	return defaultdict(rec_dd)