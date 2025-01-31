#!/usr/bin/python3
# -*- coding: utf-8 -*-


# Import sys for relative import
import sys
import os

from collections import defaultdict
import glob
import pickle
import xml

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")


from Corpus.dictionaries import Dictionary, Shelf
from Tools.download import GithubDir, File


class LSJ(Dictionary):
    def __init__(self, *args, **kw):
        super(self.__class__, self).__init__(*args, **kw)
        # Based on Perseus Digital Library
        self.sourcelang = "gr"
        self.targetlang = "en"
        self.file = GithubDir(
            "PerseusDL",
            "lexica",
            "Files/LSJ",
            sourceDir="CTS_XML_TEI/perseus/pdllex/grc/lsj"
        )
        self.posDict = None
        self.getPath(self.__class__.__name__)

    def install(self):
        return self.download()

    def download(self):
        return self.file.download()

    def installPOS(self):
        # Checking / downloading the file
        path = os.path.dirname(os.path.abspath(__file__))
        greekMorph = File(
            url="https://github.com/jfinkels/hopper/raw/master/xml/data/greek.morph.xml",
            path="Cache",
            filename="greek.morph.xml"
        )
        # Parsing it
        data = {}
        for event, elem in xml.etree.cElementTree.iterparse(greekMorph.path):
            if elem.tag == "analysis":
                lemma = {}
                for child in elem:
                    if child.tag == "lemma":
                        lemma["lemma_morph"] = child.text
                    elif child.tag == "pos":
                        lemma["pos"] = child.text
                data[lemma["lemma_morph"]] = lemma["pos"]

        with open(path + "/../Cache/greek.betacode.pos.pickle", "wb") as f:
            pickle.dump(data, f)
        return data

    def readPOS(self):
        path = os.path.dirname(os.path.abspath(__file__))
        try:
            with open(path + "/../Cache/greek.betacode.pos.pickle", "rb") as f:
                return pickle.load(f)
        except:
            return self.installPOS()

    def getPOS(self, lemma):
        if self.posDict is None:
            self.posDict = self.readPOS()
        if lemma in self.posDict:
            return self.posDict[lemma]
        return "Unknown"

    def TEIConverter(self, POS):
        """
            Common method for LS and LSJ as they share the same structure
        """
        # I think we should move from BS to something else...
        files = glob.glob('/'.join([self.file.path, '*.xml']))
        data = {}

        for pos in POS:
            data[POS[pos]] = defaultdict(list)

        pos = None

        for file in files:
            tree = xml.etree.cElementTree.parse(file)
            root = tree.getroot()
            for word in root.findall('.//entryFree'):
                orth = word.find("./orth").text
                pos_text = self.getPOS(orth)
                if pos_text in POS:
                    pos = POS[pos_text]
                    senses = word.findall('./sense/tr')
                    text = " ".join([s.text for s in senses])
                    data[pos][orth].append(self.removeStopwords(text))
        self.data = data
        return data

    def callback(self):
        return self.TEIConverter(
            POS={
                "adj": "ADJ",
                "noun": "N",
                "verb": "V"
            }
        )

    def convert(self, force=False):
        return self._convert(force, callback=self.callback)

    def check(self):
        """
            There is two type of files we need to get :
             - Betacode POS registry
             - Dictionary files
        """
        path = os.path.dirname(os.path.abspath(__file__))
        poses = path + "/../Cache/greek.betacode.pos.pickle"
        xmlFiles = len([name for name in os.listdir(path + '/../Files/LSJ') if os.path.isfile(path + "/../Files/LSJ/" + name)])
        if xmlFiles == 27 and os.path.isfile(poses):
            return True
        return False


class Greek(Shelf):
    """Corpus including all Greek Dictionaries GreekCorpus"""
    def __init__(self):
        data = {
            "LSJ": LSJ()
        }
        super(Greek, self).__init__(dictionaries=data)
