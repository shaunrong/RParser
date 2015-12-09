#!/usr/bin/env python
import copy
from collections import defaultdict

import itertools

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'


class PostProcessor(object):
    def __init__(self, verb_parent, method_parent, ioput, original_text, sub_table):
        self._verb_parent = verb_parent
        self._method_parent = method_parent
        self._ioput = ioput
        self._original_text = original_text
        self._sub_table = sub_table
        self._reverse_sub_table = defaultdict(lambda: [])
        for word, sub in self._sub_table.iteritems():
            self._reverse_sub_table[sub].append(word)

    def process(self):
        summary = {}
        if len(self._verb_parent) == 0:
            summary['state'] = 'extra information'

        if len(self._verb_parent) > 0:
            action_num = len(self._verb_parent)
            verb_node_keys = self._verb_parent.keys()
            verb_node_keys = self._sort_keys(verb_node_keys)
            for i in range(action_num):
                summary['action{}'.format(i+1)] = {}
                v = ""
                for v_pos in self._verb_parent[verb_node_keys[i]]:
                    v += v_pos[0]
                    v += ', '
                v = v[:-2]
                summary['action{}'.format(i+1)]['v'] = repr(v)
                method_seq_num = 1
                io_seq_num = 1
                for method_phrase in self._method_parent[verb_node_keys[i]]:
                    original_method_phrase = self.find_orig_phrase(method_phrase)
                    summary['action{}'.format(i+1)]['method{}'.format(method_seq_num)] = repr(original_method_phrase)
                    method_seq_num += 1
                for np in self._ioput:
                    orig_np = self.find_orig_phrase(np)
                    summary['action1']['input_output_{}'.format(io_seq_num)] = repr(orig_np)
                    io_seq_num += 1

        return summary

    def _sort_keys(self, verb_node_keys):
        if len(verb_node_keys) == 1:
            return verb_node_keys
        else:
            for i in range(len(verb_node_keys)):
                for j in range(i+1, len(verb_node_keys)):
                    self._sort_elements(verb_node_keys, i, j)
            return verb_node_keys

    def _sort_elements(self, verb_node_keys, i, j):
        if self.i_on_right(verb_node_keys[i], verb_node_keys[j]):
            tmp_list = copy.copy(verb_node_keys[j])
            verb_node_keys[j] = copy.copy(verb_node_keys[i])
            verb_node_keys[i] = tmp_list

    @staticmethod
    def i_on_right(i_list, j_list):
        compare_length = min(len(i_list), len(j_list))
        i_or_right_bool = False
        for i in range(compare_length):
            if i_list[i] > j_list[i]:
                i_or_right_bool = True
        return i_or_right_bool

    def find_orig_phrase(self, method_phrase):
        orgi_method_phrase = method_phrase
        method_phrase_word_list = method_phrase.split(' ')
        iter_list = []
        position_list = []
        for i, word in enumerate(method_phrase_word_list):
            if word == 'COMPOUND' or word == 'UNIT' or word == 'NUMBER':
                iter_list.append(self._reverse_sub_table[word])
                position_list.append(i)
        if position_list:
            for sub_comb in itertools.product(*iter_list):
                for i, pos in enumerate(position_list):
                    try:
                        method_phrase_word_list[pos] = sub_comb[i]
                    except:
                        pass
                method_phrase_word_list = self._concat_comma_pierod(method_phrase_word_list)
                method_phrase_word_list = self._recover_round_brackets(method_phrase_word_list)
                if ' '.join(method_phrase_word_list) in self._original_text:
                    orgi_method_phrase = ' '.join(method_phrase_word_list)

        return orgi_method_phrase

    @staticmethod
    def _concat_comma_pierod(method_phrase_word_list):
        word_list = []
        for i, word in enumerate(method_phrase_word_list):
            if word == unicode(',') or word == unicode('.'):
                word_list[-1] = word_list[-1] + word
            else:
                word_list.append(word)
        return word_list

    @staticmethod
    def _recover_round_brackets(method_phrase_word_list):
        orig_phrase_list = copy.copy(method_phrase_word_list)
        word_list = []
        for i, word in enumerate(orig_phrase_list):
            if word == unicode('-RRB-'):
                word_list[-1] += ')'
            elif word == unicode('-LRB-'):
                orig_phrase_list[i+1] = '(' + orig_phrase_list[i+1]
            else:
                word_list.append(word)
        return word_list
