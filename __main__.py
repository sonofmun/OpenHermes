#!/usr/bin/python3
# -*- coding: utf-8 -*-

import getopt
import sys
import os


class OpenSynonyms(object):
	def __init__(self, corpus, algorythm, name = "OpenSynonyms"):
		self.corpus = corpus
		self.algorythm = algorythm

		self.path = os.path.dirname(os.path.abspath(__file__))

		self.name = name

	def checkCacheAnalyse(self):
		return False

	def generate(self, force = False):
		""" Read and Generate the dictionaries """
		data = {}
		for lang in self.corpus:
			data[lang] = self.corpus[lang].convert(force = force)
		self.data = data
		return data

	def analyse(self, force = False, debug = False):
		""" Run the algorythm on the corpus """

		inst = algorythm(self.data)
		inst.dictConvert()
		inst.similarity()

		self.results = inst.average
		self.instance = inst

		self.to_pickle(debug = debug)
		return inst.average

	def from_pickle(self, path = None, debug = False):
		pass

	def to_pickle(self, path = None, debug = False):
		for POS in self.results:
			if not path:
				path = self.path + "Cache/"
			path = "{0}OGL_{1}_{2}_{3}_average.pickle".format(POS, self.algorythm.__name__, self.name)

			self.results[POS].to_pickle(path)
			if debug == true:
				print ("Results saved to {0}".format(path))


	def to_csv(self, path = None, debug = False):

		for POS in self.results:
			if not path:
				path = self.path + "Results/"

			path = "{0}OGL_{1}_{2}_{3}_average.csv".format(POS, self.algorythm.__name__, self.name)

			self.results[POS].to_csv(path)
			if debug == true:
				print ("Results saved to {0}".format(path))

#############################################################################################
#
#
#	Commandline part
#
#
#############################################################################################

from Corpus import latin, greek
from Corpus.collatinus import Collatinus
from Analysis import computation

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

#We set up a list of available to run corpus
#Tuples
AvailableCorpus = [
	["Greek", {
		"LSJ" : greek.LSJ()
	}, "(Greek) Corpus based on LSJ"],
	["Collatinus", {
		"en" : Collatinus("uk"),
		"fr" : Collatinus("fr"),
		"de" : Collatinus("de"),
		"ca" : Collatinus("ca"),
		"gl" : Collatinus("gl"),
		"it" : Collatinus("la"),
		"pt" : Collatinus("pt")
	}, "(Latin) Corpus based on Collatinus lexicons"]
]

AvailableAlgorythm = [
	["CosineSim", computation.CosineSim, "A Cosine similarity algorythm"]
]

if __name__ == "__main__":

	try:
		opts, args = getopt.getopt(sys.argv[1:],"hc:",["corpus=", "help", "algorythm=", "force="])
	except getopt.GetoptError:
		opts = []

	corpus = None
	algorythm = AvailableAlgorythm[0][1]
	algorythmString = AvailableAlgorythm[0][0]
	force = False

	for o in opts:
		if o[0] in ["h", "--help"]:
			print( """{0}Help for Open Philology Synonym Generator{1}

{3}Commands:{1}
{2}--corpus= , c{1}\t Define the corpus
{2}--algorythm= , a{1}\t Define the algorythm you're using
{2}--force=0{1}\t Force the reconstruction of the cache. --force=1 means you reconstruct. Default 0""".format(color.DARKCYAN, color.END, color.BLUE, color.UNDERLINE))

			print ("\n{0}Corpora:{1}".format(color.UNDERLINE, color.END))
			i = 0
			for corpus in AvailableCorpus:
				print ("{0}\t {1} \t\te.g. {4}--corpus={2}, -c{3}, -c{2}{5}".format(color.BLUE + corpus[0] + color.END, corpus[2], corpus[0], i, color.DARKCYAN, color.END))
				i += 1

			print ("\n{0}Algorythms:{1}".format(color.UNDERLINE, color.END))
			i = 0
			for algo in AvailableAlgorythm:
				print ("{0}\t {1} \t\te.g. {4}--algorythm={2}, -a {3}, -a {2}{5}".format(color.BLUE + algo[0] + color.END, algo[2], algo[0], i, color.DARKCYAN, color.END))
				i += 1
			sys.exit()
		if o[0] in ["--force"]:
			if o[1].isdigit():
				z = int(o[1])
				if z == 1:
					force = True
		if o[0] in ["c", "--corpus"]:
			if o[1].isdigit():
				z = int(o[1])
				if len(AvailableCorpus) - 1 > z:
					corpus = AvailableCorpus[z]
			else:
				match = [group for group in AvailableCorpus if group[0] == o[1]]
				if len(match) == 1:
					corpus = match[0]
		if o[0] in ["a", "--algorythm="]:
			if o[1].isdigit():
				z = int(o[1])
				if len(AvailableAlgorythm) - 1 > z:
					algorythm = AvailableAlgorythm[z][1]
					algorythmString = AvailableAlgorythm[z][0]
			else:
				match = [group for group in AvailableAlgorythm if group[0] == o[1]]
				if len(match) == 1:
					algorythm = match[0]
				else:
					print("Unknown algorythm")
					sys.exit()

	if corpus == None:
		print("Unknown Corpus")
		sys.exit()

	instance = OpenSynonyms(
			corpus = corpus[1],
			algorythm = algorythm,
			name = corpus[0]
		)
	instance.generate()
	instance.analyse()
	instance.to_csv(debug = True)