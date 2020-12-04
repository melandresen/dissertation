# Dissertation

This repository contains the data and scripts used for my PhD thesis ("Potentiale syntaktischer Annotationen für die datengeleitete Sprachbeschreibung am Beispiel der Wissenschaftssprachen der Germanistik", publication in progress). Due to copyright law, the original data of the corpus cannot be made available. Instead, this repository contains scripts and several derived data formats:

**Annotation-data** contains versions of the corpus files annotated with parts-of-speech and syntactic dependencies in conll format. For copyright reasons, the columns for token and lemma are blank.

**Frequency-data** contains csv files with all the n-gram frequencies of all texts in the corpus as they were used for the analysis. This does also include the data sets with token information.

The script **conll2frequencies.py** takes the conll files as input and produces n-gram frequencies (the step from the data in annotation-data to those in frequency-data). Note that this step can not be reproduced for the data sets including tokens as tokens are masked in the annotation-data made available here.

The script **svm.py** takes the data from frequency-data as input, trains a Support Vector Machine for each data set, extracts the feature weights and outputs the features ordered by their absolute weight to **results**.

The script **svm_crossvalidation.py** runs a crossvalidation on some of the data sets as reported in the thesis.

