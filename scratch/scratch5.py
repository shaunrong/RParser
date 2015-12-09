#!/usr/bin/env python
from RParser import RParser

from PreProcessor import PreProcessor

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'


cfuf = PreProcessor()
with open('../data/verb_method_arg/test/paper0105.raw.txt', 'r') as f:
    text = f.read().splitlines()

orig_text = text[4]

process_text, sub_table = cfuf.process([orig_text.strip()])

sen = process_text[0]

rp = RParser()

NPs = rp.return_NPs(sen)

print NPs