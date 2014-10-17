#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import sys for relative import
import sys
sys.path.append("../")

from Corpus.dictionaries import Dictionary
from Tools.download import GithubDir

from bs4 import BeautifulSoup as b_soup
from collections import defaultdict

class LSJ(Dictionary):
	def __init__(self, *args, **kw):
		super(self.__class__, self).__init__(*args, **kw)
		#Based on Perseus Digital Library
		#self.url = "https://github.com/PerseusDL/lexica/tree/master/CTS_XML_TEI/perseus/pdllex/grc/lsj/*.xml"
		self.sourcelang = "gr"
		self.targetlang = "en"

	def install(self):
		return self.download()

	def download(self):
		self.file =  GithubDir("PerseusDL", "lexica", "Files/LSJ", sourceDir = "CTS_XML_TEI/perseus/pdllex/grc/lsj")
		return self.file.download()

	def convert(self):
		tr_dict = defaultdict(list)
		for file in files:
			with open(file) as f:
				text = f.read()
			soup = b_soup(text)
			for word in soup.find_all('entryfree'):
				for s in word.find_all('sense'):
					try:
						tr_dict[word.orth.text].append(s.tr.text)
					except:
						continue
