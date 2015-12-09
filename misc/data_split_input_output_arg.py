#!/usr/bin/env python
import argparse
import os
import random
from shutil import copyfile

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, required=True, help='input file folder')
    parser.add_argument('-o', type=str, required=True, help='transfer file folder')
    args = parser.parse_args()

    distinct_files = []

    for ff in os.listdir(os.path.join(args.f, 'train')):
        file_name = ff.split('.')[0]
        if file_name not in distinct_files:
            distinct_files.append(file_name)
    for ff in os.listdir(os.path.join(args.f, 'test')):
        file_name = ff.split('.')[0]
        if file_name not in distinct_files:
            distinct_files.append(file_name)

    distinct_files = set(distinct_files)

    train_file = random.sample(distinct_files, int(0.75 * len(distinct_files)))

    for ff in os.listdir(os.path.join(args.f, 'train')):
        file_name_list = ff.split('.')
        if (file_name_list[0] in train_file) and file_name_list[1] != 'RParse':
            copyfile(os.path.join(args.f, 'train', ff), os.path.join(args.o, 'train', ff))
        if (file_name_list[0] not in train_file) and file_name_list[1] != 'RParse':
            copyfile(os.path.join(args.f, 'train', ff), os.path.join(args.o, 'test', ff))

    for ff in os.listdir(os.path.join(args.f, 'test')):
        file_name_list = ff.split('.')
        if (file_name_list[0] in train_file) and file_name_list[1] != 'RParse':
            copyfile(os.path.join(args.f, 'test', ff), os.path.join(args.o, 'train', ff))
        if (file_name_list[0] not in train_file) and file_name_list[1] != 'RParse':
            copyfile(os.path.join(args.f, 'test', ff), os.path.join(args.o, 'test', ff))

