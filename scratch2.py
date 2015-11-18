#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import nltk
import yaml
from nltk.parse import stanford

from PreProcessor import PreProcessor

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'


with open('environ.yaml', 'r') as f:
    env = yaml.load(f)

stanford_parser_folder = env['stanford_parser_folder']

os.environ['STANFORD_PARSER'] = stanford_parser_folder
os.environ['STANFORD_MODELS'] = stanford_parser_folder

cfuf = PreProcessor()
with open('data/1.raw.txt', 'r') as f:
    text = f.read().splitlines()

process_text, chemical_table, split_word = cfuf.process(text)

print process_text
print chemical_table
print split_word

sen = process_text[0]

parser = stanford.StanfordParser(model_path=env['model_path'])
sentences = parser.raw_parse(sen)

ROOT = 'ROOT'


def getNodes(parent):
    for node in parent:
        if type(node) is nltk.Tree:
            if node.label() == ROOT:
                print "======== Sentence ========="
                print "Sentence:", " ".join(node.leaves())
            else:
                print "Label:", node.label()
                print "Leaves:", node.leaves()
                print 'parents:', node.parent


            getNodes(node)
        else:
            print "Word:", node

#getNodes(tree)

for line in sentences:
    line.draw()