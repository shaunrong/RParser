#!/usr/bin/env python
import nltk
import yaml
import pickle
from nltk.classify import MaxentClassifier

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'


if __name__ == '__main__':
    with open('ioput_train_db.yaml', 'r') as f:
        train_db = yaml.load(f)
    train_set = []

    for key, value in train_db.iteritems():
        for i in value:
            feats = []
            sentences = nltk.sent_tokenize(i)
            for sen in sentences:
                feats = feats + nltk.word_tokenize(sen)

            feats = [w.lower() for w in feats]
            feats = dict([(w, True) for w in feats])
            train_set.append((feats, key))

    classifier = MaxentClassifier.train(train_set)

    with open('ioput_maxent_classifier.pickle', 'wb') as f:
        pickle.dump(classifier, f)

