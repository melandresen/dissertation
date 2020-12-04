#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.model_selection import cross_val_score


def cross_validate(file_name):
    data = pd.read_csv('frequency-data/' + file_name, sep='\t')

    labels = data['_Fach_']  # extract labels from variable '_Fach_'
    data = data.drop(['_Fach_', 'text_name'], axis=1)  # drop non-frequency variables

    data = data.div(data.sum(axis=1), axis=0)  # calculate relative frequencies

    data = data.loc[:, np.count_nonzero(data, axis=0) >= 5]  # drop features that appear in less than 5 texts

    my_svm = svm.SVC(kernel='linear')       # train svm

    scores = cross_val_score(my_svm, data, labels, cv=10, scoring='accuracy')       # get cross-val-scores
    print(scores)
    print(np.mean(scores))


files = ['1_linear_pos.txt', '1_ngrams_linear_token.txt', '3_ngrams_syntactic_token+pos.txt']

for file in files:
    cross_validate(file)
