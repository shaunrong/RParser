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
with open('data/3.raw.txt', 'r') as f:
    text = f.read().splitlines()

process_text, sub_table = cfuf.process(text)

sen = process_text[1]

print sen


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
