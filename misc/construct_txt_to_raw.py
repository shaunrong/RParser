#!/usr/bin/env python
import argparse
import os

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, required=True, help='file folder')
    args = parser.parse_args()

    for file in os.listdir(args.f):
        file_name = file.split('.')[0]
        os.rename(os.path.join(args.f, file), os.path.join(args.f, "{}.raw.txt".format(file_name)))
