#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Melanie Andresen

import os
import re
import numpy as np
import pandas as pd
from sklearn import svm


def process_file(file_name):
    print('Now working on file {}...'.format(file_name))
    data = pd.read_csv(in_dir + file_name, sep='\t')

    labels = data['_Fach_']     # extract labels from variable '_Fach_'
    data = data.drop(['_Fach_', 'text_name'], axis=1)       # drop non-frequency variables

    data = data.div(data.sum(axis=1), axis=0)       # calculate relative frequencies

    data = data.loc[:, np.count_nonzero(data, axis=0) >= 5]     # drop features that appear in less than 5 texts

    my_svm = svm.SVC(kernel='linear')       # train svm
    my_svm.fit(data, labels)

    results = pd.DataFrame({'Feature': [], 'value': []})        # extract features weights
    for i, item in enumerate(my_svm.coef_.ravel()):
        results.loc[i] = [data.columns[i], item]

    results = results.iloc[(-results['value'].abs()).argsort()]
    results.to_csv(out_dir + file_name, sep='\t')


in_dir = 'frequency-data/'
out_dir = 'results/'

files = os.listdir(in_dir)
files = [f for f in files if not re.match('\.', f)]

for file in files:
    process_file(file)
