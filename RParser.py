#!/usr/bin/env python
import copy
import os
from collections import defaultdict

import nltk
import yaml
from nltk.parse import stanford

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'


class RParser(object):
    def __init__(self):
        with open('environ.yaml', 'r') as f:
            env = yaml.load(f)

        stanford_parser_folder = env['stanford_parser_folder']
        os.environ['STANFORD_PARSER'] = stanford_parser_folder
        os.environ['STANFORD_MODELS'] = stanford_parser_folder

        self._tree_parser = stanford.StanfordParser(model_path=env['model_path'])

    def parse(self, sen):
        verb = []

        parsed_sen = self._tree_parser.raw_parse(sen)
        root_tree = parsed_sen.next()

        sen = nltk.word_tokenize(sen)
        for i, token in enumerate(sen):
            if token == '(':
                sen[i] = '-LRB-'
            if token == ')':
                sen[i] = '-RRB-'

        dfs_repr = self.build_dfs_repr(sen, root_tree)

        #Find Action Verbs
        lowest_verb_height = root_tree.height()

        for key, value in dfs_repr.iteritems():
            pointer = copy.copy(value)
            pointer.pop()
            if root_tree[tuple(pointer)].label() == 'VBN':
                if len(pointer) == lowest_verb_height:
                    verb.append(key)
                if len(pointer) < lowest_verb_height:
                    verb = [key]
                    lowest_verb_height = len(pointer)

        if len(verb) == 0:
            parsse_summary = {'state': 'extra information'}
        if len(verb) > 1:
            verb_parent = defaultdict(lambda: [])
            for v in verb:
                verb_node = copy.copy(dfs_repr[v])
                verb_node.pop()
                verb_node.pop()
                verb_parent[tuple(verb_node)].append(v)

            total_action_num = len(verb_parent)



    def build_dfs_repr(self, sen, tree):
        representation = {}
        pointer = [0]
        while type(tree[tuple(pointer)]) != unicode:
            pointer.append(0)
        if tree[tuple(pointer)] != sen[0]:
            raise ValueError('leftest pointer does not point to first work in the root tree')
        representation[sen[0], 0] = pointer
        for i in range(1, len(sen)):
            pointer, representation = self._find_right_word(sen[i], i, pointer, representation, tree)

        return representation

    def _find_right_word(self, word, idx, pointer, representation, tree):
        last_element = pointer.pop()
        while last_element == (len(tree[tuple(pointer)]) - 1):
            last_element = pointer.pop()
        pointer.append(last_element + 1)
        while type(tree[tuple(pointer)]) != unicode:
            pointer.append(0)
        if tree[tuple(pointer)] != word:
            print word, pointer, tree[tuple(pointer)]
            raise ValueError('pointer does not match word')

        representation[word, idx] = copy.copy(pointer)

        return pointer, representation