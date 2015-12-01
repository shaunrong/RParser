#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import nltk
import yaml
from nltk.parse import stanford

from PreProcessor import PreProcessor
from RParser import RParser

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
with open('data/2.raw.txt', 'r') as f:
    text = f.read().splitlines()

process_text, sub_table = cfuf.process(text)


sen = process_text[5]

rp = RParser()

verb_parent, method_parent = rp.parse(sen)

print verb_parent
print method_parent
