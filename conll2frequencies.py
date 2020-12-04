#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Melanie Andresen
# Purpose: Generate linear and syntactic n-gram frequencies from CoNLL files

import sys
from collections import Counter
import pandas as pd
from corpus_classes import Corpus
import nltk
import numpy as np


def get_syntactic_ngrams(sentence, n):

    ngrams = []

    for word in sentence.words:
        ngram = [word]
        while len(ngram) != n:
            if word.head == 0:  # abort if root node is reached
                ngram = None
                break
            word = sentence.words[word.head - 1]  # switch to head word
            ngram.append(word)  # append head word to ngram list
        if ngram:
            ngram = ngram[::-1]  # inverts order, so that the dominant item comes first
            ngrams.append(ngram)

    return ngrams


def get_ngrams(type, levels, n):

    all_frequencies = {}

    for file in corpus.files:
        file_frequencies = []
        for sentence in file.sentences:
            if n == 1 or type == 'linear':
                ngrams = [item for item in nltk.ngrams(sentence.words, n)]
            elif n > 1 and type == 'syntactic':
                ngrams = get_syntactic_ngrams(sentence, n)
            else:
                print('Unknown parameters!')
                sys.exit()
            file_frequencies.extend(ngrams)

        file_frequencies_no_punctuation = []

        for ngram in file_frequencies:  # exclude all n-grams with punctuation
            elements = [w.pos for w in ngram]
            if '$' not in ''.join(elements):
                file_frequencies_no_punctuation.append(ngram)

        file_frequencies_levels = []

        separator = '__' if type == 'linear' else '_>_'

        for ngram in file_frequencies_no_punctuation:  # apply levels
            if levels == 'token':
                elements = [w.token for w in ngram]
            elif levels == 'pos':
                elements = [w.pos for w in ngram]
            elif levels == 'deprel':
                elements = [w.deprel for w in ngram]
            elif levels == 'token+pos':
                elements = [w.token + '_' + w.pos for w in ngram]
            elif levels == 'pos+deprel':
                element_1 = [ngram[0].pos]  # only syntactic relations between the elements are included
                elements_other = [w.pos + '_' + w.deprel for w in ngram[1:]]
                elements = element_1 + elements_other
            elif levels == 'token+pos+deprel':
                element_1 = [
                    ngram[0].token + '_' + ngram[0].pos]  # only syntactic relations between the elements are included
                elements_other = [w.token + '_' + w.pos + '_' + w.deprel for w in ngram[1:]]
                elements = element_1 + elements_other
            file_frequencies_levels.append(separator.join(elements))

        all_frequencies[file.filename] = Counter(file_frequencies_levels)

    result = pd.DataFrame(all_frequencies).T
    result = result.replace(np.nan, 0)

    result.index = result.index.set_names(['text_name'])
    result = result.reset_index()

    return result


# parameters:
type = 'syntactic'
n = 3
levels = 'pos+deprel'

possible_levels = ['token', 'pos', 'deprel', 'token+pos', 'pos+deprel', 'token+pos+deprel']
if levels not in possible_levels:
    sys.exit('Unknown levels! Possible values: {}'.format(', '.join(possible_levels)))

corpus = Corpus('annotation-data/')

result = get_ngrams(type, levels, n)

result['_Fach_'] = np.where(result['text_name'].str.match('Lin'), 'Linguistik',
                            'Literaturwissenschaft')  # add variable for discipline based on file name

non_frequency_variables = ['text_name', '_Fach_']  # reorder columns and rows
result = result[non_frequency_variables + [c for c in result if c not in non_frequency_variables]]
result = result.sort_values(by=['text_name'])

result.to_csv('frequency-data/{}_{}_{}.txt'.format(n, type, levels), sep='\t', index=False)
