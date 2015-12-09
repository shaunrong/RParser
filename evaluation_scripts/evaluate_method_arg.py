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

    total_gold_methods = 0
    total_predict_methods = 0
    r_methods = 0
    p_methods = 0

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
                    method_args = []
                    for method_key in action_value.keys():
                        if 'method' in method_key:
                            total_gold_methods += 1
                            method_args.append(action_value[unicode(method_key)])
                    if action_key in predict[k].keys():
                        for method_key in predict[k][action_key].keys():
                            if 'method' in method_key:
                                if unicode(predict[k][action_key][method_key][2:-1]) in method_args:
                                    r_methods += 1

        for k, v in predict.iteritems():
            if 'state' not in v.keys():
                for action_key, action_value in v.iteritems():
                    method_args = []
                    for method_key in action_value.keys():
                        if 'method' in method_key:
                            total_predict_methods += 1
                            method_args.append(unicode(action_value[method_key][2:-1]))
                    if action_key in gold[k].keys():
                        for method_key in gold[k][action_key].keys():
                            if 'method' in method_key:
                                if unicode(gold[k][action_key][method_key]) in method_args:
                                    p_methods += 1

    recall = r_methods / float(total_gold_methods)
    precision = p_methods / float(total_predict_methods)
    f1 = 2 / (1.0 / recall + 1.0 / precision)

    print "recall for method arguments is {}".format(recall)
    print "precision for method argument is {}".format(precision)
    print "F1 score for key method argument is {}".format(f1)