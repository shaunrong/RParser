#!/usr/bin/env python
import argparse
import os

from evaluation_scripts.ioput_baseline_predict import ioput_baseline_predict

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, required=True, help='file folder')
    args = parser.parse_args()

    for ff in os.listdir(args.f):
        if ff.split('.')[1] == 'raw':
            ioput_baseline_predict(os.path.join(args.f, ff))
