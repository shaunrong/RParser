#!/usr/bin/env python
import argparse
import os

import math
import yaml

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, required=True, help='input file folder')
    args = parser.parse_args()

    distinct_file_names = []
    for file in os.listdir(args.f):
        distinct_file_names.append(file.split('.')[0])

    distinct_file_names = set(distinct_file_names)

    total_gold_verbs = 0
    total_predict_verbs = 0
    r_verbs = 0
    p_verbs = 0

    for file in distinct_file_names:
        gold_yaml_file = file + '.gold.yaml'
        predict_yaml_file = file + '.RParser.yaml'
        with open(os.path.join(args.f, gold_yaml_file), 'r') as f:
            gold = yaml.load(f)
        with open(os.path.join(args.f, predict_yaml_file), 'r') as f:
            predict = yaml.load(f)

        for k, v in gold.iteritems():
            if 'state' not in v.keys():
                for action_key, action_value in v.iteritems():
                    total_gold_verbs += 1
                    if action_key in predict[k].keys():
                        if unicode(action_value['v']) == unicode(predict[k][action_key]['v'][2:-1]):
                            r_verbs += 1

        for k, v in predict.iteritems():
            if 'state' not in v.keys():
                for action_key, action_value in v.iteritems():
                    total_predict_verbs += 1
                    if action_key in gold[k].keys():
                        if unicode(action_value['v'][2:-1]) == unicode(gold[k][action_key]['v']):
                            p_verbs += 1

    recall = r_verbs / float(total_gold_verbs)
    precision = p_verbs / float(total_predict_verbs)
    f1 = math.sqrt((recall ** 2 + precision ** 2) / 2.0)

    print "recall for key action verbs is {}".format(recall)
    print "precision for key action verbs is {}".format(precision)
    print "F1 score for key action verbs is {}".format(f1)
