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
        self._dependency_parser = stanford.StanfordDependencyParser(model_path=env['model_path'])

    # This parser returns key action verbs and method arguments associated with that key verb
    def parse(self, sen):
        ori_sen = copy.copy(sen)
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

        for i, token in enumerate(sen):
            pointer = copy.copy(dfs_repr[token, i])
            pointer.pop()
            if root_tree[tuple(pointer)].label() == 'VBN':
                if len(pointer) == lowest_verb_height:
                    verb.append((token, i))
                if len(pointer) < lowest_verb_height:
                    verb = [(token, i)]
                    lowest_verb_height = len(pointer)

        if len(verb) == 0:
            verb_parent = {}
            method_parent = {}
        if len(verb) > 0:
            verb_parent = defaultdict(lambda: [])
            method_parent = defaultdict(lambda: [])
            for v in verb:
                verb_node = copy.copy(dfs_repr[v])
                verb_node.pop()
                verb_node.pop()
                verb_parent[tuple(verb_node)].append(v)

            #Find method arguments associated with action verbs
            for k, v in verb_parent.iteritems():
                for child_phrase in root_tree[tuple(k)]:
                    if child_phrase.label() == 'PP' or child_phrase.label() == 'ADVP':
                        method_phrase = child_phrase.leaves()
                        method_parent[tuple(k)].append(' '.join(method_phrase))

            dependency_parse = self._dependency_parser.raw_parse(ori_sen)

            for k, v in verb_parent.iteritems():
                for verb in v:
                    for p in dependency_parse:
                        for t in p.triples():
                            if t[0][0] == unicode(verb[0]) and t[0][1] == unicode('VBN') and t[1] == unicode('xcomp'):
                                associate_word_list = []
                                for k_word in dfs_repr.keys():
                                    if unicode(k_word[0]) == t[2][0]:
                                        associate_word_list.append(k_word)
                                associate_word = self._find_associate_vbg(associate_word_list, verb)
                                associate_vbg_node = copy.copy(dfs_repr[associate_word])
                                associate_vbg_node.pop()
                                associate_vbg_node.pop()
                                associate_vbg_method_phrase = root_tree[tuple(associate_vbg_node)].leaves()
                                method_parent[tuple(k)].append(' '.join(associate_vbg_method_phrase))

        return verb_parent, method_parent

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

    @staticmethod
    def _find_associate_vbg(associate_word_list, verb):
        word_distance = {}
        for word in associate_word_list:
            word_distance[word] = abs(verb[1] - word[1])
        return min(word_distance, key=word_distance.get)