#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import yaml
from nltk.parse import stanford

from PreProcessor import ChemFormUnitFinder

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'


with open('environ.yaml', 'r') as f:
    env = yaml.load(f)

stanford_parser_folder = env['stanford_parser_folder']

os.environ['STANFORD_PARSER'] = stanford_parser_folder
os.environ['STANFORD_MODELS'] = stanford_parser_folder

cfuf = ChemFormUnitFinder()
with open('data/1.raw.txt', 'r') as f:
    text = f.read().splitlines()

process_text, chemical_table = cfuf.process(text)

for sen in process_text:

    parser = stanford.StanfordDependencyParser(model_path=env['model_path'])
    sentences = parser.raw_parse(sen)

    for parse in sentences:
        for t in parse.triples():
            print t

    parser = stanford.StanfordParser(model_path=env['model_path'])
    sentences = parser.raw_parse((sen))
    print sentences

    # GUI
    for line in sentences:
        line.pprint()