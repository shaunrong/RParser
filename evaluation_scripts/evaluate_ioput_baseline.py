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

    total_gold_ioputs = 0
    total_predict_ioputs = 0
    r_ioputs = 0
    p_ioputs = 0

    for file in distinct_file_names:
        gold_yaml_file = file + '.gold.yaml'
        predict_yaml_file = file + '.ioput_baseline.yaml'
        with open(os.path.join(args.f, gold_yaml_file), 'r') as f:
            gold = yaml.load(f)
        with open(os.path.join(args.f, predict_yaml_file), 'r') as f:
            predict = yaml.load(f)

        for k, v in gold.iteritems():
            if 'state' not in v.keys():
                for action_key, action_value in v.iteritems():
                    ioputs = []
                    for key, value in action_value.iteritems():
                        if ('input' in key or 'output' in key) and \
                                (value != 'implicit object' and value != 'implicit objective'):
                            total_gold_ioputs += 1
                            ioputs.append(action_value[unicode(key)])
                    if 'action1' in predict[k].keys():
                        for ioput_key in predict[k]['action1'].keys():
                            if 'input_output' in ioput_key:
                                if unicode(predict[k]['action1'][ioput_key][2:-1]) in ioputs:
                                    r_ioputs += 1.0

        for k, v in predict.iteritems():
            if 'state' not in v.keys():
                ioputs = []
                for kk, vv in v['action1'].iteritems():
                    if 'input_output' in kk:
                        total_predict_ioputs += 1
                        ioputs.append(unicode(vv[2:-1]))
                if 'state' not in gold[k].keys():
                    for action_key, action_v in gold[k].iteritems():
                        for kk, vv in action_v.iteritems():
                            if ('input' in kk or 'output' in kk) and \
                                    (vv != 'implicit object' and vv != 'implicit objective'):
                                if unicode(vv) in ioputs:
                                    p_ioputs += 1

    recall = r_ioputs / float(total_gold_ioputs)
    if recall > 1.0:
        recall = 1.0
    precision = p_ioputs / float(total_predict_ioputs)
    f1 = 2 / (1.0 / recall + 1.0 / precision)

    print "recall for input output argument is {}".format(recall)
    print "precision for input output argument is {}".format(precision)
    print "F1 score for input output argument is {}".format(f1)
