#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from nltk.parse import stanford
import sys

from ChemFormUnitFinder import ChemFormUnitFinder

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'


reload(sys)
sys.setdefaultencoding('utf8')

stanford_parser_folder = '/Users/Shaun/Documents/PhD_Course/6.806_NLP/project/RParser/resources/stanford_parser'

os.environ['STANFORD_PARSER'] = stanford_parser_folder
os.environ['STANFORD_MODELS'] = stanford_parser_folder

cfuf = ChemFormUnitFinder()
with open('data/3.raw.txt', 'r') as f:
    text = f.read().splitlines()

process_text, chemical_table = cfuf.process(text)

for sen in process_text:

    parser = stanford.StanfordDependencyParser(model_path=os.path.join(stanford_parser_folder, 'englishPCFG.ser.gz'))
    sentences = parser.raw_parse(sen)

    for parse in sentences:
        for t in parse.triples():
            print t

    parser = stanford.StanfordParser(model_path=os.path.join(stanford_parser_folder, 'englishPCFG.ser.gz'))
    sentences = parser.raw_parse((sen))
    print sentences

    # GUI
    for line in sentences:
        for sentence in line:
            sentence.draw()