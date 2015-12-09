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


def RParse_predict(ff):
    with open(ff, 'r') as f:
        text = f.read().splitlines()

    output_yaml = {}

    for i, orig_text in enumerate(text):
        rp = RParser()
        #Preprocess
        pre_p = PreProcessor()
        process_text, sub_table = pre_p.process([orig_text.strip()])
        sen = process_text[0]
        #RParse
        verb_parent, method_parent = rp.parse_v_method(sen)
        ioput_phrases = rp.parse_input_output(sen, verb_parent, method_parent)
        #Postprocess
        post_p = PostProcessor(verb_parent, method_parent, ioput_phrases, orig_text.strip(), sub_table)
        summary = post_p.process()

        output_yaml['sen{}'.format(i+1)] = summary

    file_path = ff.split('/')
    output_file_name_list = file_path[-1].split('.')
    output_file_name_list[1] = 'RParser'
    output_file_name_list[2] = 'yaml'
    file_path[-1] = '.'.join(output_file_name_list)
    output_file_path = '/'.join(file_path)
    with open(output_file_path, 'w') as f:
        f.write(yaml.dump(output_yaml, default_flow_style=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, required=True, help='input file')
    args = parser.parse_args()

    RParse_predict(args.i)
