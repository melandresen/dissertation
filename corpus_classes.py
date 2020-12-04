#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Python 3.7
# Author: Melanie Andresen (melanie.andresen@uni-hamburg.de)
# written in the context of the research project hermA (www.herma.uni-hamburg.de)
# funded by Landesforschungsförderung Hamburg

########################################################################################
# classes for representing a corpus based on CoNLL files
########################################################################################

import sys
import os
import re


class Word:
    """
    Word with linguistic features
    input: feature list as conll
    output: Word object with linguistic features
    """

    def __init__(self, word):

        feature_list = word.split('\t')  # transforms words to lists of features

        if len(feature_list) == 14:       # CoNLL 2009
            try:
                self.id = int(feature_list[0])
            except:
                raise ValueError('Sorry, unknown CoNLL format!')
            self.token = feature_list[1]
            self.lemma = feature_list[3]
            self.pos = feature_list[5]
            self.morph = feature_list[7]
            self.head = int(feature_list[9])
            self.deprel = feature_list[11]
            self.coref = ''

        elif len(feature_list) == 10:       # CoNLL-X (2006)
            self.id = int(feature_list[0])
            self.token = feature_list[1]
            self.lemma = feature_list[2]
            self.pos = feature_list[4]
            self.morph = feature_list[5]
            self.head = int(feature_list[6])
            self.deprel = feature_list[7]
            self.coref = ''

        else:
            raise ValueError('Sorry, unknown CoNLL format or empty file!')

    def __repr__(self):
        return 'Word({})'.format(self.token)


class Sentence:
    """
    List of words
    input: conll-String
    ouput: list of Word objects
    """

    def __init__(self, conll_string):

        self.words = []
        word_list = conll_string.split('\n')  # transforms sentences to lists of words
        for word in word_list:
            if not re.match('#', word):
                word = re.sub(' {2}', '\t', word)
                try:
                    self.words.append(Word(word))
                except ValueError as e:
                    raise ValueError(e)

        self.token_string = ' '.join([word.token for word in self.words])  # adds token string for readability

    def __repr__(self):
        return 'Sentence({})'.format(self.token_string)


class Text:
    """
    List of sentences
    input: path to conll-file
    output: list of Sentence objects
    """

    def __init__(self, file):
        self.path = file
        self.filename = file.split('/')[-1]
        self.sentences = []
        with open(file, 'r', encoding='utf8') as input_data:
            text = input_data.read()
        text = text.strip()
        conll_strings = text.split('\n\n')  # transforms text to list of sentences
        for conll_string in conll_strings:
            try:
                sentence = Sentence(conll_string)
                if len(sentence.words) > 0:
                    self.sentences.append(sentence)
            except ValueError as e:
                sys.exit('Text {}: {}'.format(self.path, e))


class Corpus:
    """
    List of texts
    input: path to directory
    output: list of Text objects
    """

    def __init__(self, path, files=None):

        print('Corpus is being compiled...\n')

        self.filelist = []
        if not files:
            self.filelist = os.listdir(path)
            self.filelist = [f for f in self.filelist if re.search('(conll|txt)', f)]  # reduction to txt and conll files
            self.filelist = [f for f in self.filelist if not re.match('\.', f)]  # exclusion of mac system files
        else:
            self.filelist = files

        self.files = []

        for file in self.filelist:
            self.files.append(Text(path + file))
            print('File {} imported.'.format(file))

        print('\nCorpus import finished.\n')
