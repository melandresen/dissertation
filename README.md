# Dissertation

This repository contains the data and scripts used for my PhD thesis ("Potentiale syntaktischer Annotationen für die datengeleitete Sprachbeschreibung am Beispiel der Wissenschaftssprachen der Germanistik", publication in progress). Due to copyright law, the original data of the corpus cannot be made available. Instead, this repository contains scripts and several derived data formats:

**Annotation-data** contains versions of the corpus files annotated with parts-of-speech and syntactic dependencies in conll format. For copyright reasons, the columns for token and lemma are blank.

**Frequency-data** contains csv files with all the n-gram frequencies of all texts in the corpus as they were used for the analyses without tokens. The corresponding data set with tokens can be downloaded at [https://doi.org/10.5281/zenodo.4306014](https://doi.org/10.5281/zenodo.4306014) and added to this directory for analysis.

The script **conll2frequencies.py** takes the conll files as input and produces n-gram frequencies (the step from the data in annotation-data to those in frequency-data). Parameters can be modified in lines 92-94.

The script **svm.py** takes the data from frequency-data as input, trains a support vector machine for each data set, extracts the feature weights and outputs the features ordered by their absolute weight to **results**.

The script **svm_crossvalidation.py** runs a crossvalidation on some of the data sets as reported in the thesis.

