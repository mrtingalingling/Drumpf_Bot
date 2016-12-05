#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Author: Ting'''
import logging
import traceback
import textwrap
from nltk.corpus import wordnet as wn
import enchant 
import __builtin__


POS = {
    'v': 'verb', 'a': 'adjective', 's': 'satellite adjective', 
    'n': 'noun', 'r': 'adverb'}


d = enchant.Dict("en_US")


def info(word='english', pos=None):
	if d.check(word):
		for i, syn in enumerate(wn.synsets(word, pos)):
			syns = [n.replace('_', ' ') for n in syn.lemma_names]
			ants = [a.name for m in syn.lemmas for a in m.antonyms()]
			print syns
			print ants

	def syns(): 
		return syns

	def ants(): 
		return ants

	def atn(): 
		return atns[0]

	def pos():
		return POS[syn.pos]

	# def pol(word):


if __name__ == '__main__':
	print info('rear').syns
	print info('rear').atns

# Reference
# http://stackoverflow.com/questions/21395011/python-module-with-access-to-english-dictionaries-including-definitions-of-words
# https://github.com/geekpradd/PyDictionary
# http://stackoverflow.com/questions/3788870/how-to-check-if-a-word-is-an-english-word-with-python
# http://www.velvetcache.org/2010/03/01/looking-up-words-in-a-dictionary-using-python
# http://stackoverflow.com/questions/6103907/fully-parsable-dictionary-thesaurus