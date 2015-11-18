#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
from nltk import word_tokenize


__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'


class PreProcessor(object):
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf8')
        self._chem_table = {}
        self._unit_table = {}
        self._process_text = []
        self._original_text = None
        self._elements = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
                          'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca',
                          'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Zn', 'Ga',
                          'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb',
                          'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb',
                          'Te', 'I', 'Xe', 'Cs', 'Ba', 'Hf', 'Ta', 'W', 'Re', 'Os',
                          'Ir', 'Pt', 'Au', 'Ag', 'Hg', 'Tl', 'Pb', 'Bi', 'At', 'Rn',
                          'Fr', 'Ra', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Uub',
                          'Uut', 'Uuq', 'Uup', 'Uuh', 'Uus', 'Uuo', 'La', 'Ce', 'Pr', 'Nd',
                          'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu',
                          'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es',
                          'Fm', 'Md', 'No', 'Lr']
        self._units = ['mol', 'mL', 'g', '°C', 'h', 'rpm', 'mA/g']
        self._elements.sort(key=len, reverse=True)

    def process(self, text):
        """
        :param text: a list of sentences, e.g. ["I like O2", "I hate CO2"]
        """
        self._original_text = text
        comp_ser = 1
        unit_ser = 1

        for sen in self._original_text:
            sen = unicode(sen, errors='ignore')
            sen = sen.split(' ')
            new_sen = []
            split_word = []
            for word in sen:
                if word[-1] == ',' or word[-1] == '.':
                    split_word.append(word)

            for word in sen:
                if word in split_word:
                    new_sen.append(word[0:-1])
                    new_sen.append(word[-1])
                else:
                    new_sen.append(word)
            for word in new_sen:
                token = word_tokenize(word)
                if len(token) > 1:
                    if self._is_compound(token):
                        self._chem_table[word] = 'compound'
                        comp_ser += 1
                if word in self._units:
                    self._unit_table[word] = 'unit'
                    unit_ser += 1

            for i, word in enumerate(new_sen):
                if word in self._chem_table:
                    new_sen[i] = self._chem_table[word]
                if word in self._unit_table:
                    new_sen[i] = self._unit_table[word]
            self._process_text.append(' '.join(new_sen))

        return self._process_text, self._chem_table, split_word

    def _is_compound(self, token):
        token_with_elements = 0
        for t in token:
            contain_element = False
            for e in self._elements:
                if e in t:
                    contain_element = True
            #if t == '(' or t == ')':
                #contain_element = True
            if contain_element:
                token_with_elements += 1
        if token_with_elements / float(len(token)) > 0.3:
            return True
        else:
            return False


if __name__ == '__main__':
    pp = PreProcessor()
    with open('data/1.raw.txt', 'r') as f:
        text = f.read().splitlines()
    """
    text = ['Separately, 0.02 mol of Mn(NO3)2·4H2O was dissolved in 50 mL of water to form a clear solution (A).',
            'A total of 0.02 mol of (NH4)2HPO4 and 20 g of Na2CO3 were dissolved in 100 mL of water to form a clear solution (B).',
            'Solution A was then quickly added to solution B under fast magnetic stirring.',
            'The obtained slurry was then transferred to a glass bottle sealed with a cap.',
            'The bottle was heated in a 120 °C oil bath in an Ar flushed glovebox for 4−72 h, after which it was taken out of the oil bath and slowly cooled down to room temperature.',
            'The slurry was centrifuged and washed with distilled water and methanol several times to separate the solids.',
            'The solid samples were dried in a vacuum oven at 40 °C overnight.']
    """
    print text[0]

    process_text, chem_table, split_word = pp.process([text[0]])

    print split_word
    print process_text
