#!/usr/bin/env python
import argparse

import yaml

from PostProcessor import PostProcessor
from PreProcessor import PreProcessor
from RParser import RParser

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, required=True, help='input file')
    args = parser.parse_args()

    with open(args.i, 'r') as f:
        text = f.read().splitlines()

    rp = RParser()
    output_yaml = {}

    for i, orig_text in enumerate(text):
        pre_p = PreProcessor()
        process_text, sub_table = pre_p.process([orig_text])
        sen = process_text[0]
        verb_parent, method_parent = rp.parse(sen)
        post_p = PostProcessor(verb_parent, method_parent, orig_text, sub_table)
        summary = post_p.process()
        output_yaml['sen{}'.format(i+1)] = summary

    output_file_name_list = args.i.split('.')
    output_file_name_list[1] = 'RParser'
    output_file_name_list[2] = 'yaml'
    output_file_name = '.'.join(output_file_name_list)
    with open(output_file_name, 'w') as f:
        f.write(yaml.dump(output_yaml, default_flow_style=False))
