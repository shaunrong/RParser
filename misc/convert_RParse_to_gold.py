#!/usr/bin/env python
import argparse
import os

import yaml

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, required=True, help='input rparse file')
    args = parser.parse_args()

    with open(args.i) as rparse:
        summary_rparse = yaml.load(rparse)
    summary_gold = {}
    for sen, sen_v in summary_rparse.iteritems():
        summary_gold[sen] = {}
        if 'state' in sen_v.keys():
            summary_gold[sen] = sen_v
        else:
            for action, action_v in sen_v.iteritems():
                summary_gold[sen][action] = {}
                for key, value in action_v.iteritems():
                    summary_gold[sen][action][key] = value[2:-1]
    gold_file_name_list = args.i.split('/')[-1]
    gold_file_folder = args.i.split('/')[:-1]
    gold_file_folder = '/'.join(gold_file_folder)
    gold_file_name_list = gold_file_name_list.split('.')
    gold_file_name_list[1] = 'gold'
    gold_file_name = '.'.join(gold_file_name_list)
    with open(os.path.join(gold_file_folder, gold_file_name), 'w') as f_gold:
        f_gold.write(yaml.dump(summary_gold, default_flow_style=False))
