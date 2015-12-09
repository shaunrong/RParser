#!/usr/bin/env python
import copy
import os
from collections import defaultdict

import cPickle
import nltk
import yaml
from nltk.parse import stanford

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'


class RParser(object):
    def __init__(self):
        root_folder = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(root_folder, 'environ.yaml'), 'r') as f:
            env = yaml.load(f)

        stanford_parser_folder = env['stanford_parser_folder']
        os.environ['STANFORD_PARSER'] = stanford_parser_folder
        os.environ['STANFORD_MODELS'] = stanford_parser_folder

        with open(os.path.join(root_folder, 'ioput_maxent_classifier.pickle'), 'r') as f:
            self._maxent_classifier = cPickle.loads(f.read())

        self._tree_parser = stanford.StanfordParser(model_path=env['model_path'])
        self._dependency_parser = stanford.StanfordDependencyParser(model_path=env['model_path'])

        self._NPs = []

    # This parser returns key action verbs and method arguments associated with that key verb
    def parse_v_method(self, sen):
        ori_sen = copy.copy(sen)
        verb = []

        parsed_sen = self._tree_parser.raw_parse(sen)
        root_tree = parsed_sen.next()
        """
        sen = nltk.word_tokenize(sen)
        for i, token in enumerate(sen):
            if token == '(':
                sen[i] = '-LRB-'
            if token == ')':
                sen[i] = '-RRB-'
        """
        sen = root_tree[0].leaves()
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
                    if child_phrase.label() == 'PP' or child_phrase.label() == 'ADVP' or child_phrase.label() == 'RB':
                        method_phrase = child_phrase.leaves()
                        method_parent[tuple(k)].append(' '.join(method_phrase))

            dependency_parse = self._dependency_parser.raw_parse(ori_sen)

            for k, v in verb_parent.iteritems():
                for verb in v:
                    for p in dependency_parse:
                        for t in p.triples():
                            if t[0][0] == unicode(verb[0]) and t[0][1] == unicode('VBN') and t[1] == unicode('xcomp')\
                                    and t[2][1] == unicode('VBG') and t[2][0] != unicode('then'):
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

    def parse_input_output(self, sen, verb_parent, method_parent):
        return_ioput_NP = []

        ori_sen = copy.copy(sen)

        if len(method_parent) == 0:
            return []
        else:
            method_phrases = []
            for key, values in method_parent.iteritems():
                method_phrases += values
            verb_phrases = []
            for key, values in verb_parent.iteritems():
                for verb in values:
                    verb_phrases += [verb[0]]

            parsed_sen = self._tree_parser.raw_parse(sen)
            root_tree = parsed_sen.next()

            NPs = self.return_NPs(sen)

            for NP in NPs:
                in_method_phrase = False
                for method_p in method_phrases:
                    if NP in method_p:
                        in_method_phrase = True
                if not in_method_phrase:
                    feats = self._maxent_unigram_feats(NP)
                    tag = self._maxent_classifier.classify(feats)
                    if tag == 'input_output':
                        #print NP, tag
                        return_ioput_NP.append(NP)
                final_ioput_NP = []
                for np in return_ioput_NP:
                    sub_string = False
                    for other_np in return_ioput_NP:
                        if np != other_np and (np in other_np):
                            sub_string = True
                    #debug
                    #print verb_phrases
                    #print method_phrases
                    #debug
                    for v_p in verb_phrases:
                        #print v_p
                        if v_p in np:
                            sub_string = True
                    for m_p in method_phrases:
                        if m_p in np:
                            sub_string = True
                    if not sub_string:
                        final_ioput_NP.append(np)
            return final_ioput_NP

    def return_NPs(self, sen):
        ori_sen = copy.copy(sen)
        verb = []

        parsed_sen = self._tree_parser.raw_parse(sen)
        root_tree = parsed_sen.next()

        self._add_NP(root_tree)

        return self._NPs

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

    def _add_NP(self, parent):
        for node in parent:
            if type(node) is nltk.Tree:
                if node.label() == 'NP':
                    self._NPs.append(' '.join(node.leaves()))
                self._add_NP(node)
            else:
                pass

    def _maxent_unigram_feats(self, NP):
        feats = []
        sentences = nltk.sent_tokenize(NP)
        for sen in sentences:
            feats = feats + nltk.word_tokenize(sen)

        feats = [w.lower() for w in feats]
        feats = dict([(w, True) for w in feats])
        return feats
