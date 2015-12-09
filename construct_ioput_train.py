#!/usr/bin/env python
import argparse
import os

import yaml
from nltk.parse import stanford

from PostProcessor import PostProcessor

from PreProcessor import PreProcessor

from RParser import RParser

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'


def pre_process_sub(input_output_NPs, sub_table, tree_parser):
    new_NPs = []
    for NP in input_output_NPs:
        word_list = NP.split(' ')
        for idx, word in enumerate(word_list):
            if word in sub_table.keys():
                word_list[idx] = sub_table[word]
        word_phrase = ' '.join(word_list)
        parsed_phrase = tree_parser.raw_parse(word_phrase)
        tree = parsed_phrase.next()
        new_phrase = tree.leaves()
        new_NPs.append(' '.join(new_phrase))
    return new_NPs


def extract_gold_NPs(gold_summary, sub_table, tree_parser):
    if 'state' in gold_summary.keys():
        return []
    else:
        input_output_NPs = []
        for action, action_v in gold_summary.iteritems():
            for k, v in action_v.iteritems():
                if ('input' or 'output' in k) and (v != 'implicit object' or v != 'implicit objective'):
                    input_output_NPs.append(v)

        input_output_NPs = pre_process_sub(input_output_NPs, sub_table, tree_parser)
        return input_output_NPs


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, required=True, help='file folder')
    args = parser.parse_args()

    train_file = []
    for ff in os.listdir(args.f):
        if ff.split('.')[1] == 'raw':
            train_file.append(ff.split('.')[0])

    train_file = set(train_file)

    train_summary = {}
    train_summary['input_output'] = []
    train_summary['else'] = []

    with open('environ.yaml', 'r') as f:
            env = yaml.load(f)

    stanford_parser_folder = env['stanford_parser_folder']
    os.environ['STANFORD_PARSER'] = stanford_parser_folder
    os.environ['STANFORD_MODELS'] = stanford_parser_folder

    tree_parser = stanford.StanfordParser(model_path=env['model_path'])

    for ff in train_file:
        with open(os.path.join(args.f, "{}.raw.txt".format(ff)), 'r') as f:
            text = f.read().splitlines()

        with open(os.path.join(args.f, "{}.gold.yaml".format(ff)), 'r') as f:
            gold_ticket = yaml.load(f)

        for i, orig_text in enumerate(text):
            rp = RParser()
            #Preprocess
            pre_p = PreProcessor()
            process_text, sub_table = pre_p.process([orig_text.strip()])
            sen = process_text[0]
            #RParse
            NPs = rp.return_NPs(sen)

            gold_NPs = extract_gold_NPs(gold_ticket['sen{}'.format(i+1)], sub_table, tree_parser)

            for NP in NPs:
                if NP in gold_NPs:
                    train_summary['input_output'].append(repr(NP))
                else:
                    train_summary['else'].append(repr(NP))

    with open('ioput_train_db.yaml', 'w') as f:
        f.write(yaml.dump(train_summary, default_flow_style=False))
